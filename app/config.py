# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Application Configuration"""

import json
from typing import Any, Dict

API_VERSION = "2.0"
APP_VERSION = "2.0.0-beta.8"


def load_database_config(config_file_path: str = "config.json",
                         connection_pool_size: int = 10) -> Dict[str, Any]:
    """Reads in database configuration values from a configuration
    JSON file and returns a dictionary with the values.

    :param config_file: Path to the configuration JSON file
    :type config_file: str, optional
    :param connection_pool_size: Number of connections to use in
        creating a connection pool
    :type connection_pool_size: int, optional
    :return: Dictionary containing database configuration settings
    :rtype: Dict[str, Any]
    """
    with open(config_file_path, "r") as config_file:
        config_dict = json.load(config_file)

    if "database" in config_dict:
        database_config = config_dict["database"]

        # Set database connection pooling settings if and only if there
        # is a ``use_pool`` key and it is set to True. Remove the key
        # after parsing through the configuration to prevent issues
        # with mysql.connector.connect()
        if "use_pool" in database_config and database_config["use_pool"]:
            if "pool_name" not in database_config or not database_config["pool_name"]:
                database_config["pool_name"] = "wwdtm_api"

            if "pool_size" not in database_config or not database_config["pool_size"]:
                database_config["pool_size"] = connection_pool_size

            if "pool_size" in database_config and database_config["pool_size"] < 8:
                database_config["pool_size"] = 8

            del database_config["use_pool"]
        else:
            if "pool_name" in database_config:
                del database_config["pool_name"]

            if "pool_size" in database_config:
                del database_config["pool_size"]

            if "use_pool" in config_dict["database"]:
                del database_config["use_pool"]

        return database_config
    else:
        return {}
