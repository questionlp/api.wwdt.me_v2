# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Scorekeeper endpoints"""

from app.config import API_VERSION, load_database_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import constr, PositiveInt
from wwdtm.show import details, info
from app.models.shows import (Show, Shows,
                              ShowDetails, ShowsDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/shows"
)
_database_config = load_database_config()
_database_connection = mysql.connector.connect(**_database_config)
_database_connection.autocommit = True

#region Routes
@router.get("",
            summary="Retrieve Information for All Shows",
            response_model=Shows,
            tags=["Shows"])
async def get_shows():
    """Retrieve an array of Show objects, each containing: Show ID,
    date and basic information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = info.retrieve_all(_database_connection)
        if not shows:
            raise HTTPException(status_code=404, detail="No shows found")
        else:
            return {"shows": shows}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve shows from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "shows from the database")


@router.get("/details",
            summary="Retrieve Detailed Information for All Shows",
            response_model=ShowsDetails,
            tags=["Shows"])
async def get_shows_details():
    """Retrieve an array of Show objects, each containing: Show ID,
    date, Host, Scorekeeper, Panelists, Guests and other information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = details.retrieve_all(_database_connection)
        if not shows:
            raise HTTPException(status_code=404, detail="No shows found")
        else:
            return {"shows": shows}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve shows from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "shows from the database")

#endregion
