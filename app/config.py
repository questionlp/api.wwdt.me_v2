# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Application Configuration"""

import json
from typing import Any, Dict

API_VERSION = "2.0"
APP_VERSION = "2.0.0-beta.4"


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
        if "pool_size" not in config_dict["database"]:
            config_dict["database"]["pool_size"] = connection_pool_size

        return config_dict["database"]
    else:
        return {}
