# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""FastAPI main application for api.wwdt.me"""

from os.path import exists

from fastapi import FastAPI, HTTPException
from fastapi.responses import (FileResponse,
                               HTMLResponse,
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
    swagger_ui_parameters={
        "deepLinking": False,
        "defaultModelsExpandDepth": 0,
        "syntaxHighlight.theme": "arta",
    },
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
         response_class=FileResponse)
async def robots_txt():
    """ Attempts to serve up static/robots.txt or
    static/robots.txt.dist to the requester. Raise a 404 error if
    neither file are found.
    """
    if exists("static/robots.txt"):
        return "static/robots.txt"
    elif exists("static/robots.txt.dist"):
        return "static/robots.txt.dist"
    else:
        raise HTTPException(status_code=404)


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
