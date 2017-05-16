import eventlet
eventlet.monkey_patch()

import sys

from oslo_config import cfg

from MigrationTool.worker.rpc import server as rpc_server
from MigrationTool import service
from MigrationTool import utils

CONF = cfg.CONF


def main():
    CONF(sys.argv[1:], project='MigrationTool',
         version="1.0.0")
    utils.setup_logging()

    launcher = service.get_process_launcher()
    server = service.MessagingService(
        'MigrationTool_worker', [rpc_server.WorkerServerEndpoint()],
        rpc_server.VERSION)
    launcher.launch_service(server, workers=server.get_workers_count())
    launcher.wait()


if __name__ == "__main__":
    main()
