# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
# pylint: disable=R1705
"""Application Configuration."""

import json
from pathlib import Path
from typing import Any

API_VERSION = "2.0"
APP_VERSION = "2.15.1"


def load_config(
    config_file_path: str = "config.json",
    connection_pool_size: int = 10,
    connection_pool_name: str = "wwdtm_api",
) -> dict[str, Any]:
    """Reads application and database settings from JSON file.

    :param config_file: Path to the configuration JSON file
    :type config_file: str, optional
    :param connection_pool_size: Number of connections to use in
        creating a connection pool
    :type connection_pool_size: int, optional
    :return: Dictionary containing database configuration settings
    :rtype: Dict[str, Any]
    """
    _config_file_path = Path(config_file_path)
    with _config_file_path.open(mode="r", encoding="utf-8") as config_file:
        config_dict = json.load(config_file)

    settings_config = config_dict.get("settings", None)
    settings_config["use_decimal_scores"] = bool(
        settings_config.get("use_decimal_scores", False)
    )

    if "database" in config_dict:
        database_config = config_dict["database"]

        # Set database connection pooling settings if and only if there
        # is a ``use_pool`` key and it is set to True. Remove the key
        # after parsing through the configuration to prevent issues
        # with mysql.connector.connect()
        use_pool = database_config.get("use_pool", False)

        if use_pool:
            pool_name = database_config.get("pool_name", connection_pool_name)
            pool_size = database_config.get("pool_size", connection_pool_size)
            if pool_size < connection_pool_size:
                pool_size = connection_pool_size

            database_config["pool_name"] = pool_name
            database_config["pool_size"] = pool_size
            del database_config["use_pool"]
        else:
            if "pool_name" in database_config:
                del database_config["pool_name"]

            if "pool_size" in database_config:
                del database_config["pool_size"]

            if "use_pool" in database_config:
                del database_config["use_pool"]

        return {"database": database_config, "settings": settings_config}
    else:
        return {}
