# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""FastAPI main application for api.wwdt.me."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.config import API_VERSION, APP_VERSION, load_config
from app.metadata import app_metadata, tags_metadata
from app.routers import (
    guests,
    hosts,
    locations,
    panelists,
    pronouns,
    scorekeepers,
    shows,
    version,
)

from .utility import format_umami_analytics

app = FastAPI(
    title=app_metadata["title"],
    description=app_metadata["description"].strip(),
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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
config = load_config()


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
@app.head("/", include_in_schema=False, response_class=HTMLResponse)
async def default_page(request: Request):
    """Route: Landing Page."""
    if "settings" in config and config["settings"]:
        settings = config["settings"]
        stats_url: str | None = settings.get("stats_url", None)
        patreon_url: str | None = settings.get("patreon_url", None)
        github_sponsor_url: str | None = settings.get("github_sponsor_url", None)
    else:
        stats_url = None
        patreon_url = None
        github_sponsor_url = None

    umami = config["settings"].get("umami_analytics")
    umami_analytics = format_umami_analytics(umami_analytics=umami)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stats_url": stats_url,
            "patreon_url": patreon_url,
            "github_sponsor_url": github_sponsor_url,
            "umami_analytics": umami_analytics,
        },
    )


@app.get("/favicon.ico", include_in_schema=False, response_class=RedirectResponse)
@app.head("/favicon.ico", include_in_schema=False, response_class=RedirectResponse)
async def favicon():
    """Route: favicon.ico."""
    return RedirectResponse("/static/favicon.ico", status_code=301)


@app.get("/robots.txt", include_in_schema=False)
@app.head("/robots.txt", include_in_schema=False)
async def robots_txt():
    """Route: robots.txt.

    Attempts to serve up static/robots.txt or static/robots.txt.dist to
    the requester. Raise a 404 error if neither file are found.
    """
    robots_txt_path = Path.cwd() / "static" / "robots.txt"
    robots_txt_dist_path = Path.cwd() / "static" / "robots.txt.dist"
    if robots_txt_path.exists():
        return FileResponse(path="static/robots.txt", media_type="text/plain")

    if robots_txt_dist_path.exists():
        return FileResponse(path="static/robots.txt.dist", media_type="text/plain")

    return HTTPException(status_code=404)


@app.get("/docs", include_in_schema=False, response_class=RedirectResponse)
@app.head("/docs", include_in_schema=False, response_class=RedirectResponse)
async def redoc_redirect_docs():
    """Route: Redirect /docs to specific docs path."""
    return RedirectResponse(f"/v{API_VERSION}/docs", status_code=301)


@app.get("/redoc", include_in_schema=False, response_class=RedirectResponse)
@app.head("/redoc", include_in_schema=False, response_class=RedirectResponse)
async def redoc_redirect_redoc():
    """Route: Redirect /redoc to specific docs path."""
    return RedirectResponse(f"/v{API_VERSION}/docs", status_code=301)


@app.get(
    f"/v{API_VERSION}/redoc", include_in_schema=False, response_class=RedirectResponse
)
@app.head(
    f"/v{API_VERSION}/redoc", include_in_schema=False, response_class=RedirectResponse
)
async def redoc_redirect_sub():
    """Route: Redirect for /docs."""
    return RedirectResponse(f"/v{API_VERSION}/docs", status_code=301)


@app.get("/v1.0", include_in_schema=False, response_class=RedirectResponse)
@app.head("/v1.0", include_in_schema=False, response_class=RedirectResponse)
async def api_v1_redirect():
    """Route: Redirect /v1.0 to Landing Page."""
    return RedirectResponse("/", status_code=301)


@app.get("/v1.0/docs", include_in_schema=False, response_class=RedirectResponse)
@app.head("/v1.0/docs", include_in_schema=False, response_class=RedirectResponse)
async def api_v1_docs_redirect():
    """Route: Redirect /v1.0/docs to Landing Page."""
    return RedirectResponse("/", status_code=301)


# Add the router modules for Guests, Hosts, Locations, Panelists,
# Scorekeepers, Shows and Version
app.include_router(guests.router)
app.include_router(hosts.router)
app.include_router(locations.router)
app.include_router(panelists.router)
app.include_router(pronouns.router)
app.include_router(scorekeepers.router)
app.include_router(shows.router)
app.include_router(version.router)
