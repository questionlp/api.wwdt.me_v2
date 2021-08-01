# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI main application for api.wwdt.me"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from app.config import APP_VERSION
from app.metadata import api_metadata, tags_metadata
from app.routers import (guests,
                         hosts,
                         locations,
                         panelists,
                         scorekeepers,
                         shows,
                         version,
                         )

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=api_metadata["title"],
        description=api_metadata["description"],
        routes=app.routes,
        tags=tags_metadata,
        version=APP_VERSION,
        contact={
            "name": "Linh Pham",
            "email": "dev@wwdt.me",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        }
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(guests.router)
app.include_router(hosts.router)
app.include_router(locations.router)
app.include_router(panelists.router)
app.include_router(scorekeepers.router)
app.include_router(version.router)

#region Routes
@app.get("/", include_in_schema=False,
         response_class=RedirectResponse)
async def default_page():
    return "/docs"

#endregion
