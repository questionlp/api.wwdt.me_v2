# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Scorekeeper endpoints"""

from datetime import date

from app.config import API_VERSION, load_database_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import conint
from wwdtm.show import Show
from app.models.shows import (Show as ModelsShow,
                              ShowDates as ModelsShowDates,
                              Shows as ModelsShows,
                              ShowDetails as ModelsShowDetails,
                              ShowsDetails as ModelsShowsDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/shows"
)
_database_config = load_database_config()
_database_connection = mysql.connector.connect(**_database_config)
_database_connection.autocommit = True


# region Routes
@router.get("",
            summary="Retrieve Information for All Shows",
            response_model=ModelsShows,
            tags=["Shows"])
@router.head("",
             include_in_schema=False)
async def get_shows():
    """Retrieve an array of Show objects, each containing: Show ID,
    date and basic information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_all()
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


@router.get("/id/{show_id}",
            summary="Retrieve Information by Show ID",
            response_model=ModelsShow,
            tags=["Shows"])
@router.head("/id/{show_id}",
             include_in_schema=False)
async def get_show_by_id(show_id: conint(ge=0, lt=2**31)):
    """Retrieve a Show object, based on Show ID, containing: Show ID,
    date and basic information."""
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_by_id(show_id)
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


@router.get("/date/iso/{show_date}",
            summary="Retrieve Information for Shows by Year, Month, and Day using ISO format date",
            response_model=ModelsShow,
            tags=["Shows"])
@router.head("/date/iso/{show_date}",
             include_in_schema=False)
async def get_show_by_date_string(show_date: date):
    """Retrieve a Show object, based on show date in ISO format
    (YYYY-MM-DD), containing: Show ID, date and basic information."""
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_by_date_string(show_date.isoformat())
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


@router.get("/date/{year}",
            summary="Retrieve Information for Shows by Year",
            response_model=ModelsShows,
            tags=["Shows"])
@router.head("/date/{year}",
             include_in_schema=False)
async def get_shows_by_year(year: conint(ge=1998, le=9999)):
    """Retrieve an array of Show objects, based on year, containing:
    Show ID, date and basic information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_by_year(year)
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
            response_model=ModelsShows,
            tags=["Shows"])
@router.head("/date/{year}/{month}",
             include_in_schema=False)
async def get_shows_by_year_month(year: conint(ge=1998, le=9999),
                                  month: conint(ge=1, le=12)):
    """Retrieve an array of Show objects, based on year and month,
    containing: Show ID, date and basic information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_by_year_month(year, month)
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
            response_model=ModelsShow,
            tags=["Shows"])
@router.head("/date/{year}/{month}/{day}",
             include_in_schema=False)
async def get_show_by_date(year: conint(ge=1998, le=9999),
                           month: conint(ge=1, le=12),
                           day: conint(ge=1, le=31)):
    """Retrieve a Show object, based on year, month and day, containing:
    Show ID, date and basic information."""
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_by_date(year, month, day)
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


@router.get("/dates",
            summary="Retrieve All Show Dates",
            response_model=ModelsShowDates,
            tags=["Shows"])
@router.head("/dates",
             include_in_schema=False)
async def get_all_show_dates():
    """Retrieve an array of all show dates in ISO format (YYYY-MM-DD).

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_all_dates()
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
            response_model=ModelsShowsDetails,
            tags=["Shows"])
@router.head("/details",
             include_in_schema=False)
async def get_shows_details():
    """Retrieve an array of Show objects, each containing: Show ID,
    date, Host, Scorekeeper, Panelists, Guests and other information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_all_details()
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


@router.get("/details/date/iso/{show_date}",
            summary="Retrieve Detailed Information for Shows by Year, Month, and Day using ISO format date",
            response_model=ModelsShowDetails,
            tags=["Shows"])
@router.head("/details/date/iso/{show_date}",
             include_in_schema=False)
async def get_show_details_by_date_string(show_date: date):
    """Retrieve an array of Show objects, based on show date in ISO
    format (YYYY-MM-DD), containing: Show ID, date, Host, Scorekeeper,
    Panelists, Guests and other information."""
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_details_by_date_string(show_date.isoformat())
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


@router.get("/details/date/{year}",
            summary="Retrieve Detailed Information for Shows by Year",
            response_model=ModelsShowsDetails,
            tags=["Shows"])
@router.head("/details/date/{year}",
             include_in_schema=False)
async def get_shows_details_by_year(year: conint(ge=1998, le=9999)):
    """Retrieve an array of Show objects, based on year, containing:
    Show ID, date, Host, Scorekeeper, Panelists, Guests and other
    information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_details_by_year(year)
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


@router.get("/details/date/{year}/{month}",
            summary="Retrieve Detailed Information for Shows by Year and Month",
            response_model=ModelsShowsDetails,
            tags=["Shows"])
@router.head("/details/date/{year}/{month}",
             include_in_schema=False)
async def get_shows_details_by_year_month(year: conint(ge=1998, le=9999),
                                          month: conint(ge=1, le=12)):
    """Retrieve an array of Show objects, based on year and month,
    containing: Show ID, date, Host, Scorekeeper, Panelists, Guests and
    other information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_details_by_year_month(year, month)
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


@router.get("/details/date/{year}/{month}/{day}",
            summary="Retrieve Detailed Information for a Show by Year, Month, and Day",
            response_model=ModelsShowDetails,
            tags=["Shows"])
@router.head("/details/date/{year}/{month}/{day}",
             include_in_schema=False)
async def get_show_details_by_date(year: conint(ge=1998, le=9999),
                                   month: conint(ge=1, le=12),
                                   day: conint(ge=1, le=31)):
    """Retrieve a Show object, based on year, month and day, containing:
    Show ID, date, Host, Scorekeeper, Panelists, Guests and other
    information."""
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_details_by_date(year, month, day)
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


@router.get("/details/id/{show_id}",
            summary="Retrieve Detailed Information by Show ID",
            response_model=ModelsShowDetails,
            tags=["Shows"])
@router.head("/details/id/{show_id}",
             include_in_schema=False)
async def get_show_details_by_id(show_id: conint(ge=0, lt=2**31)):
    """Retrieve a Show object, based on Show ID, containing: Show ID,
    date, Host, Scorekeeper, Panelists, Guests and other information."""
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_details_by_id(show_id)
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


@router.get("/details/recent",
            summary="Retrieve Detailed Information for Recent Shows",
            response_model=ModelsShowsDetails,
            tags=["Shows"])
@router.head("/details/recent",
             include_in_schema=False)
async def get_shows_recent_details():
    """Retrieve an array of Show objects for recent shows, each
    containing: Show ID, date, Host, Scorekeeper, Panelists, Guests
    and other information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_recent_details()
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


@router.get("/recent",
            summary="Retrieve Information for Recent Shows",
            response_model=ModelsShows,
            tags=["Shows"])
@router.head("/recent",
             include_in_schema=False)
async def get_shows_recent():
    """Retrieve an array of Show objects for recent shows, each
    containing: Show ID, date and basic information.

    Results are sorted by show date."""
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_recent()
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

# endregion
