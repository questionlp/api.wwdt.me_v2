# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI main application for api.wwdt.me"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from wwdtm import VERSION as wwdtm_version

from app.dependencies import API_VERSION, APP_VERSION
from app.metadata import tags_metadata
from app.routers import (guests,
                         hosts,
                         locations,
                         panelists,
                         scorekeepers,
                         shows,
                         )

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Wait Wait Stats API",
        version=API_VERSION,
        description="OpenAPI schema for the Wait Wait Don't Tell Me! Stats API",
        routes=app.routes,
        tags=tags_metadata
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(guests.router)
app.include_router(hosts.router)
app.include_router(locations.router)

#region Routes
@app.get("/", include_in_schema=False,
         response_class=RedirectResponse)
async def default_page():
    return "/docs"

#endregion
