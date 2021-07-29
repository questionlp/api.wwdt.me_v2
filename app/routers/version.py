# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI app version router module for api.wwdt.me"""

from app.dependencies import API_VERSION, APP_VERSION
from fastapi import APIRouter
from pydantic import BaseModel
from wwdtm import VERSION as wwdtm_version

#region Version Models
class Version(BaseModel):
    api: str
    app: str
    wwdtm: str

#endregion

router = APIRouter(
    prefix=f"/v{API_VERSION}/version"
)

#region Routes
@router.get("/",
            summary="Get API and Application Version Information",
            response_model=Version, tags=["Version"])
async def get_version():
    """Retrurn API, application and wwdtm library version infromation"""
    return {
        "api": API_VERSION,
        "app": APP_VERSION,
        "wwdtm": wwdtm_version,
    }

#endregion
