from MigrationTool import constants
from MigrationTool import exception
from MigrationTool.providers import openstack
from MigrationTool.providers import vmware_vsphere


EXPORT_PROVIDERS = {
    constants.PLATFORM_VMWARE_VSPHERE: vmware_vsphere.ExportProvider
}

IMPORT_PROVIDERS = {
    constants.PLATFORM_OPENSTACK: openstack.ImportProvider
}


def get_provider(platform_name, provider_type, event_handler):
    if provider_type == constants.PROVIDER_TYPE_EXPORT:
        cls = EXPORT_PROVIDERS.get(platform_name)
    elif provider_type == constants.PROVIDER_TYPE_IMPORT:
        cls = IMPORT_PROVIDERS.get(platform_name)

    if not cls:
        raise exception.NotFound("Provider not found: %s" % platform_name)
    return cls(event_handler)
