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
from app.models.shows import (Show, ShowDates, Shows,
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
            raise HTTPException(status_code=404,
                                detail="No shows found")
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
            raise HTTPException(status_code=404,
                                detail="No shows found")
        else:
            return {"shows": shows}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve shows from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "shows from the database")


@router.get("/dates",
            summary="Retrieve All Show Dates",
            response_model=ShowDates,
            tags=["Shows"])
async def get_all_show_dates():
    """Retrieve an array of all show dates in ISO format (YYYY-MM-DD).

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = info.retrieve_all_dates(_database_connection)
        if not shows:
            raise HTTPException(status_code=404,
                                detail="No shows found")
        else:
            return {"shows": shows}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve shows from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "shows from the database")


@router.get("/recent",
            summary="Retrieve Information for Recent Shows",
            response_model=Shows,
            tags=["Shows"])
async def get_shows_recent():
    """Retrieve an array of Show objects for recent shows, each
    containing: Show ID, date and basic information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = info.retrieve_recent(_database_connection)
        if not shows:
            raise HTTPException(status_code=404,
                                detail="No recent shows found")
        else:
            return {"shows": shows}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve shows from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "shows from the database")


@router.get("/recent/details",
            summary="Retrieve Detailed Information for Recent Shows",
            response_model=ShowsDetails,
            tags=["Shows"])
async def get_shows_recent_details():
    """Retrieve an array of Show objects for recent shows, each
    containing: Show ID, date, Host, Scorekeeper, Panelists, Guests
    and other information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = details.retrieve_recent(_database_connection)
        if not shows:
            raise HTTPException(status_code=404,
                                detail="No recent shows found")
        else:
            return {"shows": shows}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve shows from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "shows from the database")


@router.get("/date/iso/{show_date}",
            summary="Retrieve Information ",
            response_model=Show,
            tags=["Shows"])
async def get_show_by_date_string(show_date: constr(strip_whitespace=True)):
    """Retrieve a Show object, based on show date in ISO format
    (YYYY-MM-DD), containing: Show ID, date and basic information."""
    try:
        _database_connection.reconnect()
        show_info = info.retrieve_by_date_string(show_date,
                                                 _database_connection)
        if not show_info:
            raise HTTPException(status_code=404,
                                detail=f"Show date {show_date} not found")
        else:
            return show_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Show date {show_date} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/date/iso/{show_date}/details",
            summary="Retrieve Detailed Information for Shows by Year, Month, and Day",
            response_model=ShowDetails,
            tags=["Shows"])
async def get_show_details_by_date(show_date: constr(strip_whitespace=True)):
    """Retrieve an array of Show objects, based on show date in ISO
    format (YYYY-MM-DD), containing: Show ID, date, Host, Scorekeeper,
    Panelists, Guests and other information."""
    try:
        _database_connection.reconnect()
        show_details = details.retrieve_by_date_string(show_date,
                                                       _database_connection)
        if not show_details:
            raise HTTPException(status_code=404,
                                detail=f"Show date {show_date} not found")
        else:
            return show_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Show date {show_date} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/date/{year}",
            summary="Retrieve Information for Shows by Year",
            response_model=Shows,
            tags=["Shows"])
async def get_shows_by_year(year: PositiveInt):
    """Retrieve an array of Show objects, based on year, containing:
    Show ID, date and basic information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = info.retrieve_by_year(year, _database_connection)
        if not shows:
            raise HTTPException(status_code=404,
                                detail=f"Shows for {year:04d} not found")
        else:
            return {"shows": shows}
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Shows for {year:04d} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/date/{year}/details",
            summary="Retrieve Detailed Information for Shows by Year",
            response_model=ShowsDetails,
            tags=["Shows"])
async def get_shows_details_by_year(year: PositiveInt):
    """Retrieve an array of Show objects, based on year, containing:
    Show ID, date, Host, Scorekeeper, Panelists, Guests and other
    information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = details.retrieve_by_year(year, _database_connection)
        if not shows:
            raise HTTPException(status_code=404,
                                detail=f"Shows for {year:04d} not found")
        else:
            return {"shows": shows}
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Shows for {year:04d} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/date/{year}/{month}",
            summary="Retrieve Information for Shows by Year and Month",
            response_model=Shows,
            tags=["Shows"])
async def get_shows_by_year_month(year: PositiveInt,
                                  month: PositiveInt):
    """Retrieve an array of Show objects, based on year and month,
    containing: Show ID, date and basic information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = info.retrieve_by_year_month(year, month, _database_connection)
        if not shows:
            raise HTTPException(status_code=404,
                                detail=f"Shows for {year:04d}-{month:02d} not found")
        else:
            return {"shows": shows}
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Shows for {year:04d}-{month:02d} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/date/{year}/{month}/details",
            summary="Retrieve Detailed Information for Shows by Year and Month",
            response_model=ShowsDetails,
            tags=["Shows"])
async def get_shows_details_by_year_month(year: PositiveInt,
                                          month: PositiveInt):
    """Retrieve an array of Show objects, based on year and month,
    containing: Show ID, date, Host, Scorekeeper, Panelists, Guests and
    other information.

    Results are sorted by show date."""
    try:
        _database_connection.reconnect()
        shows = details.retrieve_by_year_month(year, month, _database_connection)
        if not shows:
            raise HTTPException(status_code=404,
                                detail=f"Shows for {year:04d}-{month:02d} not found")
        else:
            return {"shows": shows}
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Shows for {year:04d}-{month:02d} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/date/{year}/{month}/{day}",
            summary="Retrieve Information for a Show by Year, Month, and Day",
            response_model=Show,
            tags=["Shows"])
async def get_show_by_date(year: PositiveInt,
                           month: PositiveInt,
                           day: PositiveInt):
    """Retrieve a Show object, based on year, month and day, containing:
    Show ID, date and basic information."""
    try:
        _database_connection.reconnect()
        show_info = info.retrieve_by_date(year, month, day,
                                          _database_connection)
        if not show_info:
            raise HTTPException(status_code=404,
                                detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found")
        else:
            return show_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/date/{year}/{month}/{day}/details",
            summary="Retrieve Detailed Information for a Show by Year, Month, and Day",
            response_model=ShowDetails,
            tags=["Shows"])
async def get_show_details_by_date(year: PositiveInt,
                                   month: PositiveInt,
                                   day: PositiveInt):
    """Retrieve a Show object, based on year, month and day, containing:
    Show ID, date, Host, Scorekeeper, Panelists, Guests and other
    information."""
    try:
        _database_connection.reconnect()
        show_details = details.retrieve_by_date(year, month, day,
                                                _database_connection)
        if not show_details:
            raise HTTPException(status_code=404,
                                detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found")
        else:
            return show_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/{show_id}",
            summary="Retrieve Information by Show ID",
            response_model=Show,
            tags=["Shows"])
async def get_show_by_id(show_id: PositiveInt):
    """Retrieve a Show object, based on Show ID, containing: Show ID,
    date and basic information."""
    try:
        _database_connection.reconnect()
        show_info = info.retrieve_by_id(show_id, _database_connection)
        if not show_info:
            raise HTTPException(status_code=404,
                                detail=f"Show ID {show_id} not found")
        else:
            return show_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Show ID {show_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")


@router.get("/{show_id}/details",
            summary="Retrieve Detailed Information by Show ID",
            response_model=ShowDetails,
            tags=["Shows"])
async def get_show_details_by_id(show_id: PositiveInt):
    """Retrieve a Show object, based on Show ID, containing: Show ID,
    date, Host, Scorekeeper, Panelists, Guests and other information."""
    try:
        _database_connection.reconnect()
        show_details = details.retrieve_by_id(show_id, _database_connection)
        if not show_details:
            raise HTTPException(status_code=404,
                                detail=f"Show ID {show_id} not found")
        else:
            return show_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Show ID {show_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve show information from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "show information from the database")

#endregion
