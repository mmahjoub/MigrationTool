from pyVmomi import vim

from MigrationTool import constants


GUEST_ID_OS_TYPE_MAP = {
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNetStandard64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.win95Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.centosGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.other24xLinux64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.fedoraGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.asianux3Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.slesGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwin11Guest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwin13_64Guest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.win31Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel3Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.openServer6Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winVista64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.windows7Server64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.solaris6Guest:
    constants.OS_TYPE_SOLARIS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel7Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.solaris7Guest:
    constants.OS_TYPE_SOLARIS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian6_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian7_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winLonghorn64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwin11_64Guest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.mandrakeGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winVistaGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.windows7Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sles10_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.windows7_64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.solaris10_64Guest:
    constants.OS_TYPE_SOLARIS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNTGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sles12_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNetDatacenter64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.win98Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNetWebGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.genericLinuxGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwin10_64Guest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.netware6Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian7Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.freebsd64Guest:
    constants.OS_TYPE_BSD,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.solaris10Guest:
    constants.OS_TYPE_SOLARIS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.other24xLinuxGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.windows8Server64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.fedora64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian6Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.win2000AdvServGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.nld9Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.asianux4_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel7_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwin12_64Guest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sles10Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwinGuest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.solaris8Guest:
    constants.OS_TYPE_SOLARIS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.win2000ProGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winMeGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.eComStation2Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNetStandardGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.mandrivaGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.opensuse64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.suseGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.windows8_64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.windowsHyperVGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel2Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel5Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.other3xLinuxGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.netware4Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.other26xLinuxGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.opensuseGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winXPHomeGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.openServer5Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winLonghornGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sles11_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel4Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel6_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian5_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sles12Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.solaris11_64Guest:
    constants.OS_TYPE_SOLARIS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.oesGuest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.turboLinux64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.centos64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.oracleLinuxGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.oracleLinux64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.os2Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian4Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.otherGuest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sles11Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.windows8Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.netware5Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.other3xLinux64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.mandriva64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.other26xLinux64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.ubuntuGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNetDatacenterGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.otherGuest64:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.suse64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.redhatGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.vmkernelGuest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winXPPro64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.unixWare7Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.otherLinux64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.turboLinuxGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.dosGuest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.otherLinuxGuest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwin10Guest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian5Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.win2000ServGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel4_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel5_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.debian4_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.ubuntu64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.asianux4Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNetEnterprise64Guest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.darwin64Guest:
    constants.OS_TYPE_OS_X,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sjdsGuest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.rhel6Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.freebsdGuest:
    constants.OS_TYPE_BSD,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.eComStationGuest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.sles64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.asianux3_64Guest:
    constants.OS_TYPE_LINUX,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winNetEnterpriseGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.winXPProGuest:
    constants.OS_TYPE_WINDOWS,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.vmkernel5Guest:
    None,
    vim.vm.GuestOsDescriptor.GuestOsIdentifier.solaris9Guest:
    constants.OS_TYPE_SOLARIS,
}
