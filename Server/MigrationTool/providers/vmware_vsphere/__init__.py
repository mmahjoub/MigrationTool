import os
import re
import sys
import time
from urllib import request

import eventlet
from oslo_config import cfg
from oslo_log import log as logging
from pyVim import connect
from pyVmomi import vim

from MigrationTool import constants
from MigrationTool import exception
from MigrationTool.providers import base
from MigrationTool.providers.vmware_vsphere import guestid
from MigrationTool import utils

vmware_vsphere_opts = [
    cfg.StrOpt('vdiskmanager_path',
               default='vmware-vdiskmanager',
               help='The vmware-vdiskmanager path.'),
]

CONF = cfg.CONF
CONF.register_opts(vmware_vsphere_opts, 'vmware_vsphere')

LOG = logging.getLogger(__name__)


class ExportProvider(base.BaseExportProvider):
    def validate_connection_info(self, connection_info):
        return True

    @utils.retry_on_error()
    def _convert_disk_type(self, disk_path, target_disk_path, target_type=0):
        utils.exec_process([CONF.vmware_vsphere.vdiskmanager_path, "-r",
                            disk_path, "-t", str(target_type),
                            target_disk_path])

    def _wait_for_task(self, task):
        while task.info.state not in [vim.TaskInfo.State.success,
                                      vim.TaskInfo.State.error]:
            time.sleep(.1)
        if task.info.state == vim.TaskInfo.State.error:
            raise exception.MigrationToolException(task.info.error.msg)

    @utils.retry_on_error()
    def _connect(self, host, username, password, port, context):
        LOG.info("Connecting to: %s:%s" % (host, port))
        return connect.SmartConnect(
            host=host,
            user=username,
            pwd=password,
            port=port,
            sslContext=context)

    def _wait_for_vm_status(self, vm, status, max_wait=120):
        i = 0
        while i < max_wait and vm.runtime.powerState != status:
            time.sleep(1)
            i += 1
        return i < max_wait

    def _get_vm(self, si, instance_path):
        vm = None
        container = si.content.rootFolder
        path_items = [p.replace('\\/', '/') for p in
                      re.split(r'(?<!\\)/', instance_path)]
        if len(path_items) == 1:
            if len(container.childEntity) > 1:
                raise exception.InvalidInput(
                    "There's more than one container in the VMWare root "
                    "folder, please specify the full path for the VM, e.g. "
                    "\"Datacenter1/VM1\"")
            else:
                container = container.childEntity[0].vmFolder

        LOG.debug("VM path items:", path_items)
        for i, path_item in enumerate(path_items):
            l = [o for o in container.childEntity if o.name == path_item]
            if not l:
                raise exception.InstanceNotFound(instance_name=instance_path)
            item = l[0]
            if (i + 1 == len(path_items) and
                    isinstance(item, vim.VirtualMachine)):
                vm = item
            elif isinstance(item, vim.Datacenter):
                container = item.vmFolder
            else:
                container = item

        if vm is None:
            raise exception.InstanceNotFound(instance_name=instance_path)

        return vm

    @utils.retry_on_error()
    def _get_vm_info(self, si, instance_path):

        LOG.info("Retrieving data for VM: %s" % instance_path)
        vm = self._get_vm(si, instance_path)

        firmware_type_map = {
            vim.vm.GuestOsDescriptor.FirmwareType.bios: 'BIOS',
            vim.vm.GuestOsDescriptor.FirmwareType.efi: 'EFI'}

        vm_info = {
            'num_cpu': vm.config.hardware.numCPU,
            'num_cores_per_socket': vm.config.hardware.numCoresPerSocket,
            'memory_mb':  vm.config.hardware.memoryMB,
            'firmware_type':  firmware_type_map[vm.config.firmware],
            'nested_virtualization': vm.config.nestedHVEnabled,
            'dynamic_memory_enabled':
                not vm.config.memoryReservationLockedToMax,
            'name': vm.config.name,
            'guest_id': vm.config.guestId,
            'os_type': guestid.GUEST_ID_OS_TYPE_MAP.get(vm.config.guestId),
            'id': vm._moId,
        }

        LOG.info("vm info: %s" % str(vm_info))

        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOff:
            power_off = True
            if (vm.guest.toolsRunningStatus !=
                    vim.vm.GuestInfo.ToolsRunningStatus.guestToolsNotRunning):
                self._event_manager.progress_update("Shutting down guest OS")
                vm.ShutdownGuest()
                if self._wait_for_vm_status(
                        vm, vim.VirtualMachinePowerState.poweredOff):
                    power_off = False

            if power_off:
                self._event_manager.progress_update(
                    "Powering off the virtual machine")
                task = vm.PowerOff()
                self._wait_for_task(task)

        disk_ctrls = []
        devices = [d for d in vm.config.hardware.device if
                   isinstance(d, vim.vm.device.VirtualController)]
        for device in devices:
            ctrl_type = None
            if isinstance(device, vim.vm.device.VirtualPCIController):
                ctrl_type = "PCI"
            elif isinstance(device, vim.vm.device.VirtualSIOController):
                ctrl_type = "SIO"
            elif isinstance(device, vim.vm.device.VirtualIDEController):
                ctrl_type = "IDE"
            elif isinstance(device, vim.vm.device.VirtualSATAController):
                ctrl_type = "SATA"
            elif isinstance(device, vim.vm.device.VirtualSCSIController):
                ctrl_type = "SCSI"
            else:
                continue
            disk_ctrls.append({'id': device.key, 'type': ctrl_type,
                               'bus_number': device.busNumber})

        disks = []
        devices = [d for d in vm.config.hardware.device if
                   isinstance(d, vim.vm.device.VirtualDisk)]
        for device in devices:
            disks.append({'size': device.capacityInBytes,
                          'address': device.unitNumber,
                          'id': device.key,
                          'controller_id': device.controllerKey})

        cdroms = []
        devices = [d for d in vm.config.hardware.device if
                   isinstance(d, vim.vm.device.VirtualCdrom)]
        for device in devices:
            cdroms.append({'address': device.unitNumber, 'id': device.key,
                           'controller_id': device.controllerKey})

        floppy = []
        devices = [d for d in vm.config.hardware.device if
                   isinstance(d, vim.vm.device.VirtualFloppy)]
        for device in devices:
            floppy.append({'address': device.unitNumber, 'id': device.key,
                           'controller_id': device.controllerKey})

        nics = []
        devices = [d for d in vm.config.hardware.device if
                   isinstance(d, vim.vm.device.VirtualEthernetCard)]
        for device in devices:
            nics.append({'mac_address': device.macAddress, 'id': device.key,
                         'name': device.deviceInfo.label,
                         'network_name': device.backing.network.name})

        serial_ports = []
        devices = [d for d in vm.config.hardware.device if
                   isinstance(d, vim.vm.device.VirtualSerialPort)]
        for device in devices:
            serial_ports.append({'id': device.key})

        boot_order = []
        for boot_device in vm.config.bootOptions.bootOrder:
            if isinstance(boot_device, vim.vm.BootOptions.BootableDiskDevice):
                boot_order.append({"type": "disk",
                                   "id": boot_device.deviceKey})
            elif isinstance(boot_device,
                            vim.vm.BootOptions.BootableCdromDevice):
                boot_order.append({"type": "cdrom", "id": None})
            elif isinstance.append(boot_device,
                                   vim.vm.BootOptions.BootableEthernetDevice):
                boot_order.append({"type": "ethernet",
                                   "id": boot_device.deviceKey})
            elif isinstance(boot_device,
                            vim.vm.BootOptions.BootableFloppyDevice):
                boot_order.append({"type": "floppy", "id": None})

        vm_info["devices"] = {
            "nics": nics,
            "controllers": disk_ctrls,
            "disks": disks,
            "cdroms": cdroms,
            "floppy": floppy,
        }
        vm_info["boot_order"] = boot_order

        return vm_info, vm

    @utils.retry_on_error()
    def _export_disks(self, vm, export_path, context):
        disk_paths = []
        lease = vm.ExportVm()
        while True:
            if lease.state == vim.HttpNfcLease.State.ready:
                try:
                    tot_downloaded_bytes = 0
                    for du in [du for du in lease.info.deviceUrl if du.disk]:
                        # Key format: '/vm-70/VirtualLsiLogicController0:0'
                        ctrl_str, address = du.key[
                            du.key.rindex('/') + 1:].split(':')

                        def _get_class_name(obj):
                            return obj.__class__.__name__.split('.')[-1]

                        for i, ctrl in enumerate(
                            [d for d in vm.config.hardware.device if
                             isinstance(
                                d, vim.vm.device.VirtualController) and
                                ctrl_str.startswith(_get_class_name(d))]):
                            if int(ctrl_str[len(_get_class_name(ctrl)):]) == i:
                                disk_key = [
                                    d for d in vm.config.hardware.device if
                                    isinstance(
                                        d, vim.vm.device.VirtualDisk) and
                                    d.controllerKey == ctrl.key and
                                    d.unitNumber == int(address)][0].key
                                break

                        response = request.urlopen(du.url, context=context)
                        path = os.path.join(export_path, du.targetId)
                        disk_paths.append({'path': path, 'id': disk_key})

                        LOG.info("Downloading: %s" % path)
                        with open(path, 'wb') as f:
                            while True:
                                chunk = response.read(1024 * 1024)
                                if not chunk:
                                    break
                                tot_downloaded_bytes += len(chunk)
                                f.write(chunk)
                                lease.HttpNfcLeaseProgress(
                                    int(tot_downloaded_bytes * 100 /
                                        (lease.info.totalDiskCapacityInKB *
                                         1024)))

                    lease.HttpNfcLeaseComplete()
                    return disk_paths
                except:
                    lease.HttpNfcLeaseAbort()
                    raise
            elif lease.state == vim.HttpNfcLease.State.error:
                raise exception.MigrationToolException(lease.error.msg)
            else:
                time.sleep(.1)

    def export_instance(self, ctxt, connection_info, instance_name,
                        export_path):
        host = connection_info["host"]
        port = connection_info.get("port", 443)
        username = connection_info["username"]
        password = connection_info["password"]
        allow_untrusted = connection_info.get("allow_untrusted", False)

        # pyVmomi locks otherwise
        sys.modules['socket'] = eventlet.patcher.original('socket')
        ssl = eventlet.patcher.original('ssl')

        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        if allow_untrusted:
            context.verify_mode = ssl.CERT_NONE

        self._event_manager.set_total_progress_steps(4)

        self._event_manager.progress_update("Connecting to vSphere host")
        si = self._connect(host, username, password, port, context)
        try:
            self._event_manager.progress_update(
                "Retrieving virtual machine data")
            vm_info, vm = self._get_vm_info(si, instance_name)
            self._event_manager.progress_update("Exporting disks")
            disk_paths = self._export_disks(vm, export_path, context)
        finally:
            connect.Disconnect(si)

        self._event_manager.progress_update("Converting virtual disks format")
        for disk_path in disk_paths:
            path = disk_path["path"]
            LOG.info("Converting VMDK type: %s" % path)
            tmp_path = "%s.tmp" % path
            self._convert_disk_type(path, tmp_path)
            os.remove(path)
            os.rename(tmp_path, path)

            disks = vm_info["devices"]["disks"]
            disk_info = [d for d in disks if d["id"] == disk_path["id"]][0]
            disk_info["path"] = os.path.abspath(path)
            disk_info["format"] = constants.DISK_FORMAT_VMDK

        return vm_info
