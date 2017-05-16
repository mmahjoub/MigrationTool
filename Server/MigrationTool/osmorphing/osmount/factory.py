import itertools

from oslo_log import log as logging

from MigrationTool import constants
from MigrationTool import exception
from MigrationTool.osmorphing.osmount import ubuntu
from MigrationTool.osmorphing.osmount import windows

LOG = logging.getLogger(__name__)


def get_os_mount_tools(os_type, connection_info, event_manager,
                       ignore_devices):
    os_mount_tools = {constants.OS_TYPE_LINUX: [ubuntu.UbuntuOSMountTools],
                      constants.OS_TYPE_WINDOWS: [windows.WindowsMountTools]}

    if os_type and os_type not in os_mount_tools:
        raise exception.MigrationToolException("Unsupported OS type: %s" % os_type)

    for cls in os_mount_tools.get(os_type,
                                  itertools.chain(*os_mount_tools.values())):
        tools = cls(connection_info, event_manager, ignore_devices)
        LOG.debug("Testing OS mount tools: %s", cls.__name__)
        if tools.check_os():
            return tools
    raise exception.MigrationToolException("OS mount tools not found")
