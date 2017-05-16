import itertools

from oslo_log import log as logging

from MigrationTool import constants
from MigrationTool import exception
from MigrationTool.osmorphing import debian
from MigrationTool.osmorphing import oracle
from MigrationTool.osmorphing import redhat
from MigrationTool.osmorphing import suse
from MigrationTool.osmorphing import ubuntu
from MigrationTool.osmorphing import windows

LOG = logging.getLogger(__name__)


def get_os_morphing_tools(conn, os_type, os_root_dir, target_hypervisor,
                          target_platform, event_manager):
    os_morphing_tools_clss = {
        constants.OS_TYPE_LINUX: [debian.DebianMorphingTools,
                                  ubuntu.UbuntuMorphingTools,
                                  oracle.OracleMorphingTools,
                                  redhat.RedHatMorphingTools,
                                  suse.SUSEMorphingTools],
        constants.OS_TYPE_WINDOWS: [windows.WindowsMorphingTools],
        }

    if os_type and os_type not in os_morphing_tools_clss:
        raise exception.MigrationToolException("Unsupported OS type: %s" % os_type)

    for cls in os_morphing_tools_clss.get(
            os_type, itertools.chain(*os_morphing_tools_clss.values())):
        tools = cls(conn, os_root_dir, target_hypervisor, target_platform,
                    event_manager)
        LOG.debug("Testing OS morphing tools: %s", cls.__name__)
        os_info = tools.check_os()
        if os_info:
            return (tools, os_info)
    raise exception.MigrationToolException(
        "Cannot find the morphing tools for this OS image")
