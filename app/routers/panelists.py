# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Panelists endpoints"""

from app.config import API_VERSION, load_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import constr, PositiveInt
from wwdtm.panelist import details, info
from app.models.panelists import (Panelist, Panelists,
                                  PanelistDetails, PanelistsDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/panelists"
)
_app_config = load_config()
_database_connection = mysql.connector.connect(**_app_config)
_database_connection.autocommit = True

#region Routes
@router.get("/", summary="Retrieve Information for All Panelists",
            response_model=Panelists, tags=["Panelists"])
async def get_panelists():
    """Retrieve an array of Panelist objects, each containing: Panelist
    ID, name, slug string, and gender.

    Results are sorted by panelist name."""
    try:
        _database_connection.reconnect()
        panelists = info.retrieve_all(_database_connection)
        if not panelists:
            raise HTTPException(status_code=404, detail="No panelists found")
        else:
            return {"panelists": panelists}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve panelists from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "panelists from the database")


@router.get("/details",
            summary="Retrieve Information, Statistics, and Appearances for All Panelists",
            response_model=PanelistsDetails, tags=["Panelists"])
async def get_panelists_details():
    """Retrieve an array of Panelists objects, each containing:
    Panelists ID, name, slug string, gender, and their statistics
    and appearance details.

    Results are sorted by panelist name, with panelist apperances
    sorted by show date."""
    try:
        _database_connection.reconnect()
        panelists = details.retrieve_all(_database_connection)
        if not panelists:
            raise HTTPException(status_code=404, detail="No panelists found")
        else:
            return {"panelists": panelists}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve panelists from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "panelists from the database")


@router.get("/{panelist_id}",
            summary="Retrieve Information by Panelist ID",
            response_model=Panelist, tags=["Panelists"])
async def get_panelist_by_id(panelist_id: PositiveInt):
    """Retrieve a Panelist object, based on Panelist ID, containing:
    Panelist ID, name, slug string, and gender."""
    try:
        _database_connection.reconnect()
        panelist_info = info.retrieve_by_id(panelist_id, _database_connection)
        if not panelist_info:
            raise HTTPException(status_code=404,
                                detail=f"Panelist ID {panelist_id} not found")
        else:
            return panelist_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve panelist information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve panelist information")


@router.get("/{panelist_id}/details",
            summary="Retrieve Information, Statistics, and Appearances by Panelist ID",
            response_model=PanelistDetails, tags=["Panelists"])
async def get_panelist_details_by_id(panelist_id: PositiveInt):
    """Retrieve a Panelist object, based on Panelist ID, containing:
    Panelist ID, name, slug string, gender, and their statistics and
    appearance details.

    Panelist appearances are sorted by show date."""
    try:
        _database_connection.reconnect()
        panelist_details = details.retrieve_by_id(panelist_id, _database_connection)
        if not panelist_details:
            raise HTTPException(status_code=404,
                                detail=f"Panelist ID {panelist_id} not found")
        else:
            return panelist_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve panelist information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve panelist information")


@router.get("/slug/{panelist_slug}",
            summary="Retrieve Information by Panelist Slug String",
            response_model=Panelist, tags=["Panelists"])
async def get_panelist_by_slug(panelist_slug: constr(strip_whitespace = True)):
    """Retrieve a Panelist object, based on Panelist slug string,
    containing: Panelist ID, name, slug string, and gender."""
    try:
        _database_connection.reconnect()
        panelist_info = info.retrieve_by_slug(panelist_slug, _database_connection)
        if not panelist_info:
            raise HTTPException(status_code=404,
                                detail=f"Panelist slug string {panelist_slug} not found")
        else:
            return panelist_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve panelist information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve panelist information")


@router.get("/slug/{panelist_slug}/details",
            summary="Retrieve Information, Statistics and Appearances by Panelist by Slug String",
            response_model=PanelistDetails, tags=["Panelists"])
async def get_panelist_details_by_slug(panelist_slug: constr(strip_whitespace = True)):
    """Retrieve a Panelist object, based on Panelist slug string,
    containing: Panelist ID, name, slug string, gender, and their
    statistics and appearance details.

    Panelist appearances are sorted by show date."""
    try:
        _database_connection.reconnect()
        panelist_details = details.retrieve_by_slug(panelist_slug, _database_connection)
        if not panelist_details:
            raise HTTPException(status_code=404,
                                detail=f"Panelist ID {panelist_slug} not found")
        else:
            return panelist_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve panelist information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve panelist information")


#endregion
