# Copyright (c) 2018-2026 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Application Version endpoints."""

import mysql.connector
from fastapi import APIRouter
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm import VERSION as WWDTM_VERSION
from wwdtm import database_version

from app.config import API_VERSION, APP_VERSION, load_config
from app.models.version import Version

router = APIRouter(prefix=f"/v{API_VERSION}/version")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Wait Wait Stats API and Application Version Information",
    response_model=Version,
    tags=["Version"],
)
@router.head("", include_in_schema=False)
async def get_version():
    """Retrieves API, Application and Wait Wait Stats Library Versions."""
    _database_version = database_version(database_connection=_database_connection)

    return {
        "api": API_VERSION,
        "app": APP_VERSION,
        "database": ".".join(str(segment) for segment in _database_version),
        "wwdtm": WWDTM_VERSION,
    }
