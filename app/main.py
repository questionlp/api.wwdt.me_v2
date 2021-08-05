# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI main application for api.wwdt.me"""

from fastapi import FastAPI
from fastapi.responses import (HTMLResponse,
                               PlainTextResponse,
                               RedirectResponse,
                               )
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.config import APP_VERSION
from app.metadata import app_description, app_title, tags_metadata
from app.routers import (guests,
                         hosts,
                         locations,
                         panelists,
                         scorekeepers,
                         shows,
                         version,
                         )

app = FastAPI(
    title=app_title,
    description=app_description,
    openapi_tags=tags_metadata,
    version=APP_VERSION,
    contact={
        "name": "Linh Pham",
        "email": "dev@wwdt.me",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_url="/v2.0/openapi.json",
    redoc_url="/v2.0/docs",
    docs_url="/v2.0/openapi",
)

app.mount("/static",
          StaticFiles(directory="static"),
          name="static",
          )
templates = Jinja2Templates(directory="templates")

#region Generic Routes
@app.get("/",
         include_in_schema=False,
         response_class=HTMLResponse,
         )
async def default_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request} )

@app.get("/favicon.ico",
         include_in_schema=False,
         response_class=RedirectResponse,
         )
async def favicon():
    return RedirectResponse("/static/favicon.ico", status_code=301)

@app.get("/robots.txt",
         include_in_schema=False,
         response_class=PlainTextResponse,
         )
async def robots_txt():
    return ""

@app.get("/docs",
         include_in_schema=False,
         response_class=RedirectResponse,
         )
async def redoc_redirect():
    return RedirectResponse("/v2.0/docs", status_code=301)

@app.get("/redoc",
         include_in_schema=False,
         response_class=RedirectResponse,
         )
async def redoc_redirect():
    return RedirectResponse("/v2.0/docs", status_code=301)

@app.get("/v2.0/redoc",
         include_in_schema=False,
         response_class=RedirectResponse,
         )
async def redoc_redirect_sub():
    return RedirectResponse("/v2.0/docs", status_code=301)


#endregion

# Add the router modules for Guests, Hosts, Locations, Panelists,
# Scorekeepers, Shows and Version
app.include_router(guests.router)
app.include_router(hosts.router)
app.include_router(locations.router)
app.include_router(panelists.router)
app.include_router(scorekeepers.router)
app.include_router(shows.router)
app.include_router(version.router)
