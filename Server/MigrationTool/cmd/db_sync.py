import sys

from oslo_config import cfg

from MigrationTool.db import api as db_api
from MigrationTool import utils

CONF = cfg.CONF


def main():
    CONF(sys.argv[1:], project='MigrationTool',
         version="1.0.0")
    utils.setup_logging()

    db_api.db_sync(db_api.get_engine())


if __name__ == "__main__":
    main()
