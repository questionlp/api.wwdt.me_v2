# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""API routes for Application Version endpoints"""

from app.config import API_VERSION, APP_VERSION
from fastapi import APIRouter
from wwdtm import VERSION as WWDTM_VERSION
from app.models.version import Version

router = APIRouter(
    prefix=f"/v{API_VERSION}/version"
)


# region Routes
@router.get("",
            summary="Retrieve Wait Wait Stats API and Application Version Information",
            response_model=Version,
            tags=["Version"])
@router.head("",
             include_in_schema=False)
async def get_version():
    """Retrieve Wait Wait Stats API version, application version, and
    wwdtm library version"""
    return {
        "api": API_VERSION,
        "app": APP_VERSION,
        "wwdtm": WWDTM_VERSION,
    }

# endregion
