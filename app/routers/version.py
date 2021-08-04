# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Application Version endpoints"""

from app.config import API_VERSION, APP_VERSION
from fastapi import APIRouter
from pydantic import BaseModel, Field
from wwdtm import VERSION as wwdtm_version

#region Version Models
class Version(BaseModel):
    """Wait Wait Stats API and Application Version Information"""
    api: str = Field(title="Wait Wait Stats API Version")
    app: str = Field(title="Application Version")
    wwdtm: str = Field(title="wwdtm Version")

#endregion

router = APIRouter(
    prefix=f"/v{API_VERSION}/version"
)

#region Routes
@router.get("",
            summary="Retrieve Wait Wait Stats API and Application Version Information",
            response_model=Version,
            tags=["Version"])
async def get_version():
    """Retrieve Wait Wait Stats API version, application version, and
    wwdtm library version"""
    return {
        "api": API_VERSION,
        "app": APP_VERSION,
        "wwdtm": wwdtm_version,
    }

#endregion
