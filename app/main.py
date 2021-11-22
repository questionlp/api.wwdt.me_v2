# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI main application for api.wwdt.me"""

from fastapi import FastAPI
from fastapi.responses import (HTMLResponse,
                               PlainTextResponse,
                               RedirectResponse)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.config import API_VERSION, APP_VERSION
from app.metadata import (app_metadata,
                          tags_metadata)
from app.routers import (guests,
                         hosts,
                         locations,
                         panelists,
                         scorekeepers,
                         shows,
                         version)

app = FastAPI(
    title=app_metadata["title"],
    description=app_metadata["description"],
    openapi_tags=tags_metadata,
    version=APP_VERSION,
    contact=app_metadata["contact_info"],
    license_info=app_metadata["license_info"],
    openapi_url=f"/v{API_VERSION}/openapi.json",
    redoc_url=f"/v{API_VERSION}/docs",
    docs_url=f"/v{API_VERSION}/openapi",
)

app.mount("/static",
          StaticFiles(directory="static"),
          name="static")
templates = Jinja2Templates(directory="templates")


# region Generic Routes
@app.get("/",
         include_in_schema=False,
         response_class=HTMLResponse)
async def default_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico",
         include_in_schema=False,
         response_class=RedirectResponse)
async def favicon():
    return RedirectResponse("/static/favicon.ico", status_code=301)


@app.get("/robots.txt",
         include_in_schema=False,
         response_class=PlainTextResponse)
async def robots_txt():
    return ""


@app.get("/docs",
         include_in_schema=False,
         response_class=RedirectResponse)
async def redoc_redirect_docs():
    return RedirectResponse(f"/v{API_VERSION}/docs", status_code=301)


@app.get("/redoc",
         include_in_schema=False,
         response_class=RedirectResponse)
async def redoc_redirect_redoc():
    return RedirectResponse(f"/v{API_VERSION}/docs", status_code=301)


@app.get(f"/v{API_VERSION}/redoc",
         include_in_schema=False,
         response_class=RedirectResponse)
async def redoc_redirect_sub():
    return RedirectResponse(f"/v{API_VERSION}/docs", status_code=301)

# endregion

# Add the router modules for Guests, Hosts, Locations, Panelists,
# Scorekeepers, Shows and Version
app.include_router(guests.router)
app.include_router(hosts.router)
app.include_router(locations.router)
app.include_router(panelists.router)
app.include_router(scorekeepers.router)
app.include_router(shows.router)
app.include_router(version.router)
