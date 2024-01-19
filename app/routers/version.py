# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Application Version endpoints."""

from fastapi import APIRouter
from wwdtm import VERSION as WWDTM_VERSION

from app.config import API_VERSION, APP_VERSION
from app.models.version import Version

router = APIRouter(prefix=f"/v{API_VERSION}/version")


@router.get(
    "",
    summary="Retrieve Wait Wait Stats API and Application Version Information",
    response_model=Version,
    tags=["Version"],
)
@router.head("", include_in_schema=False)
async def get_version():
    """Retrieves API, Application and Wait Wait Stats Library Versions."""
    return {
        "api": API_VERSION,
        "app": APP_VERSION,
        "wwdtm": WWDTM_VERSION,
    }
