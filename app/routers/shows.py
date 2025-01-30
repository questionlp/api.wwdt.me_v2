# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Scorekeeper endpoints."""

from datetime import date
from typing import Annotated

import mysql.connector
from fastapi import APIRouter, HTTPException, Path
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.show import Show

from app.config import API_VERSION, load_config
from app.models.shows import Show as ModelsShow
from app.models.shows import ShowDates as ModelsShowDates
from app.models.shows import ShowDetails as ModelsShowDetails
from app.models.shows import Shows as ModelsShows
from app.models.shows import ShowsDetails as ModelsShowsDetails

router = APIRouter(prefix=f"/v{API_VERSION}/shows")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Shows",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("", include_in_schema=False)
async def get_shows():
    """Retrieve All Shows.

    Returned data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_all()
        if shows:
            return {"shows": shows}

        raise HTTPException(status_code=404, detail="No shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving shows from the database",
        ) from None


@router.get(
    "/best-ofs",
    summary="Retrieve Information for All Best Of Shows",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("/best-ofs", include_in_schema=False)
async def get_best_ofs():
    """Retrieve all Best Of Shows.

    Returned data: Show ID, date, Best Of flag, Repeat flag and  NPR.org
    show url
    """
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_all_best_ofs()
        if show_info:
            return {"shows": show_info}

        raise HTTPException(status_code=404, detail="No Best Of shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve Best Of shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving Best Of shows from the database",
        ) from None


@router.get(
    "/id/{show_id}",
    summary="Retrieve Information by Show ID",
    response_model=ModelsShow,
    tags=["Shows"],
)
@router.head("/id/{show_id}", include_in_schema=False)
async def get_show_by_id(
    show_id: Annotated[int, Path(title="The ID of the show to get", ge=0, lt=2**31)],
):
    """Retrieve a Show by Show ID.

    Returned data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL
    """
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_by_id(show_id)
        if show_info:
            return show_info

        raise HTTPException(status_code=404, detail=f"Show ID {show_id} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Show ID {show_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/date/iso/{show_date}",
    summary="Retrieve Information for Shows by Year, Month, and Day using ISO format date",
    response_model=ModelsShow,
    tags=["Shows"],
)
@router.head("/date/iso/{show_date}", include_in_schema=False)
async def get_show_by_date_string(
    show_date: Annotated[date, Path(title="ISO date for the show to get")],
):
    """Retrieve a Show by Show Date in YYYY-MM-DD format.

    Returned data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL
    """
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_by_date_string(show_date.isoformat())
        if show_info:
            return show_info

        raise HTTPException(status_code=404, detail=f"Show date {show_date} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Show date {show_date} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/date/{year}",
    summary="Retrieve Information for Shows by Year",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("/date/{year}", include_in_schema=False)
async def get_shows_by_year(
    year: Annotated[int, Path(title="The year to get shows for", ge=1998, le=9999)],
):
    """Retrieve All Shows by Year.

    Returned data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_by_year(year)
        if shows:
            return {"shows": shows}

        raise HTTPException(status_code=404, detail=f"Shows for {year:04d} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Shows for {year:04d} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/date/{year}/{month}",
    summary="Retrieve Information for Shows by Year and Month",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("/date/{year}/{month}", include_in_schema=False)
async def get_shows_by_year_month(
    year: Annotated[int, Path(title="The year to get shows for", ge=1998, le=9999)],
    month: Annotated[int, Path(title="The month to get shows for", ge=1, le=12)],
):
    """Retrieve All Shows by Year and Month.

    Returned data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_by_year_month(year, month)
        if shows:
            return {"shows": shows}

        raise HTTPException(
            status_code=404, detail=f"Shows for {year:04d}-{month:02d} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Shows for {year:04d}-{month:02d} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/date/month-day/{month}/{day}",
    summary="Retrieve Information for Shows by Month and Day",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("/date/month-day/{month}/{day}", include_in_schema=False)
async def get_show_by_month_day(
    month: Annotated[int, Path(title="The month to get shows for", ge=1, le=12)],
    day: Annotated[int, Path(title="The day to get shows for", ge=1, le=31)],
):
    """Retrieve All Shows by Month and Day.

    Returned data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_by_month_day(month, day)
        if shows:
            return {"shows": shows}

        raise HTTPException(
            status_code=404,
            detail=f"Shows for month {month:02d} and {day:02d} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Shows for month {month:02d} and {day:02d} not found",
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/date/{year}/{month}/{day}",
    summary="Retrieve Information for a Show by Year, Month, and Day",
    response_model=ModelsShow,
    tags=["Shows"],
)
@router.head("/date/{year}/{month}/{day}", include_in_schema=False)
async def get_show_by_date(
    year: Annotated[int, Path(title="The year to get a show for", ge=1998, le=9999)],
    month: Annotated[int, Path(title="The month to get a show for", ge=1, le=12)],
    day: Annotated[int, Path(title="The day to get a show for", ge=1, le=31)],
):
    """Retrieve a Show by Year, Month and Day.

    Returned data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL
    """
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_by_date(year, month, day)
        if show_info:
            return show_info

        raise HTTPException(
            status_code=404,
            detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found",
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/dates",
    summary="Retrieve All Show Dates",
    response_model=ModelsShowDates,
    tags=["Shows"],
)
@router.head("/dates", include_in_schema=False)
async def get_all_show_dates():
    """Retrieve All Show Dates.

    Returned data: Show dates in YYYY-MM-DD format
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_all_dates()
        if shows:
            return {"shows": shows}

        raise HTTPException(status_code=404, detail="No shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving shows from the database",
        ) from None


@router.get(
    "/details",
    summary="Retrieve Detailed Information for All Shows",
    response_model=ModelsShowsDetails,
    tags=["Shows"],
)
@router.head("/details", include_in_schema=False)
async def get_shows_details():
    """Retrieve Details For All Shows.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_all_details(
            include_decimal_scores=_config["settings"]["use_decimal_scores"]
        )
        if shows:
            return {"shows": shows}

        raise HTTPException(status_code=404, detail="No shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving shows from the database",
        ) from None


@router.get(
    "/details/best-ofs",
    summary="Retrieve Detailed Information for All Best Of Shows",
    response_model=ModelsShowDetails,
    tags=["Shows"],
)
@router.head("/details/best-ofs", include_in_schema=False)
async def get_details_best_ofs():
    """Retrieve all Best Of Shows.

    Returned data: Show ID, date, Best Of flag, Repeat flag and  NPR.org
    show url
    """
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_all_best_ofs_details()
        if show_details:
            return show_details

        raise HTTPException(status_code=404, detail="No Best Of shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve Best Of shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving Best Of shows from the database",
        ) from None


@router.get(
    "/details/id/{show_id}",
    summary="Retrieve Detailed Information by Show ID",
    response_model=ModelsShowDetails,
    tags=["Shows"],
)
@router.head("/details/id/{show_id}", include_in_schema=False)
async def get_show_details_by_id(
    show_id: Annotated[int, Path(title="The ID of the show to get", ge=0, lt=2**31)],
):
    """Retrieve Details for a Shows by Show ID.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests
    """
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_details_by_id(
            show_id, include_decimal_scores=_config["settings"]["use_decimal_scores"]
        )
        if show_details:
            return show_details

        raise HTTPException(status_code=404, detail=f"Show ID {show_id} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Show ID {show_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/details/date/iso/{show_date}",
    summary="Retrieve Detailed Information for Shows by Year, Month, and Day using ISO format date",
    response_model=ModelsShowDetails,
    tags=["Shows"],
)
@router.head("/details/date/iso/{show_date}", include_in_schema=False)
async def get_show_details_by_date_string(
    show_date: Annotated[date, Path(title="ISO date for the show to get")],
):
    """Retrieve Details for a Show by Show Date in YYYY-MM-DD format.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests
    """
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_details_by_date_string(
            show_date.isoformat(),
            include_decimal_scores=_config["settings"]["use_decimal_scores"],
        )
        if show_details:
            return show_details

        raise HTTPException(status_code=404, detail=f"Show date {show_date} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Show date {show_date} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/details/date/{year}",
    summary="Retrieve Detailed Information for Shows by Year",
    response_model=ModelsShowsDetails,
    tags=["Shows"],
)
@router.head("/details/date/{year}", include_in_schema=False)
async def get_shows_details_by_year(
    year: Annotated[int, Path(title="The year to get shows for", ge=1998, le=9999)],
):
    """Retrieve Details for Shows by Year.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_details_by_year(
            year, include_decimal_scores=_config["settings"]["use_decimal_scores"]
        )
        if shows:
            return {"shows": shows}

        raise HTTPException(status_code=404, detail=f"Shows for {year:04d} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Shows for {year:04d} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/details/date/{year}/{month}",
    summary="Retrieve Detailed Information for Shows by Year and Month",
    response_model=ModelsShowsDetails,
    tags=["Shows"],
)
@router.head("/details/date/{year}/{month}", include_in_schema=False)
async def get_shows_details_by_year_month(
    year: Annotated[int, Path(title="The year to get shows for", ge=1998, le=9999)],
    month: Annotated[int, Path(title="The month to get shows for", ge=1, le=12)],
):
    """Retrieve Details for Shows by Year and Month.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_details_by_year_month(
            year,
            month,
            include_decimal_scores=_config["settings"]["use_decimal_scores"],
        )
        if shows:
            return {"shows": shows}

        raise HTTPException(
            status_code=404, detail=f"Shows for {year:04d}-{month:02d} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Shows for {year:04d}-{month:02d} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/details/date/month-day/{month}/{day}",
    summary="Retrieve Detailed Information for Shows by Month and Day",
    response_model=ModelsShowsDetails,
    tags=["Shows"],
)
@router.head("/details/date/month-day/{month}/{day}", include_in_schema=False)
async def get_show_details_by_month_day(
    month: Annotated[int, Path(title="The month to get shows for", ge=1, le=12)],
    day: Annotated[int, Path(title="The day to get shows for", ge=1, le=31)],
):
    """Retrieve Details for Shows by Month and Day.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_details_by_month_day(
            month, day, include_decimal_scores=_config["settings"]["use_decimal_scores"]
        )
        if shows:
            return {"shows": shows}

        raise HTTPException(
            status_code=404,
            detail=f"Shows for month {month:02d} and day {day:02d} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Shows for month {month:02d} and day {day:02d} not found",
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/details/date/{year}/{month}/{day}",
    summary="Retrieve Detailed Information for a Show by Year, Month, and Day",
    response_model=ModelsShowDetails,
    tags=["Shows"],
)
@router.head("/details/date/{year}/{month}/{day}", include_in_schema=False)
async def get_show_details_by_date(
    year: Annotated[int, Path(title="The year to get a show for", ge=1998, le=9999)],
    month: Annotated[int, Path(title="The month to get a show for", ge=1, le=12)],
    day: Annotated[int, Path(title="The day to get a show for", ge=1, le=31)],
):
    """Retrieve Details for a Shows by Year, Month and Day.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests
    """
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_details_by_date(
            year,
            month,
            day,
            include_decimal_scores=_config["settings"]["use_decimal_scores"],
        )
        if show_details:
            return show_details

        raise HTTPException(
            status_code=404,
            detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Shows for {year:04d}-{month:02d}-{day:02d} not found",
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve show information from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving show information from the database",
        ) from None


@router.get(
    "/details/recent",
    summary="Retrieve Detailed Information for Recent Shows",
    response_model=ModelsShowsDetails,
    tags=["Shows"],
)
@router.head("/details/recent", include_in_schema=False)
async def get_shows_recent_details():
    """Retrieve Details for Recent Shows.

    Return data: Show ID, date, Best Of flag, Repeat flag or date,
    NPR.org show URL, location, description, notes, host, scorekeeper,
    panelists, Bluff information and Not My Job guests

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_recent_details(
            include_decimal_scores=_config["settings"]["use_decimal_scores"]
        )
        if shows:
            return {"shows": shows}

        raise HTTPException(status_code=404, detail="No recent shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving shows from the database",
        ) from None


@router.get(
    "/details/repeat-best-ofs",
    summary="Retrieve Detailed Information for All Repeat Best Of Shows",
    response_model=ModelsShowDetails,
    tags=["Shows"],
)
@router.head("/details/repeat-best-ofs", include_in_schema=False)
async def get_details_repeat_best_ofs():
    """Retrieve all Repeat Best Of Shows.

    Returned data: Show ID, date, Best Of flag, Repeat flag and  NPR.org
    show url
    """
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_all_repeat_best_ofs_details()
        if show_details:
            return show_details

        raise HTTPException(status_code=404, detail="No Repeat Best Of shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve Repeat Best Of shows from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving Repeat Best Of shows from "
            "the database",
        ) from None


@router.get(
    "/details/repeats",
    summary="Retrieve Detailed Information for All Repeat Shows",
    response_model=ModelsShowDetails,
    tags=["Shows"],
)
@router.head("/details/repeats", include_in_schema=False)
async def get_details_repeats():
    """Retrieve all Repeat Shows.

    Returned data: Show ID, date, Best Of flag, Repeat flag and  NPR.org
    show url
    """
    try:
        show = Show(database_connection=_database_connection)
        show_details = show.retrieve_all_repeats_details()
        if show_details:
            return show_details

        raise HTTPException(status_code=404, detail="No Repeat shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve Repeat shows from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving Repeat shows from the database",
        ) from None


@router.get(
    "/recent",
    summary="Retrieve Information for Recent Shows",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("/recent", include_in_schema=False)
async def get_shows_recent():
    """Retrieve Recent Shows.

    Return data: Show ID, date, Best Of flag, Repeat flag and NPR.org
    show URL

    Shows are sorted by date.
    """
    try:
        show = Show(database_connection=_database_connection)
        shows = show.retrieve_recent()
        if shows:
            return {"shows": shows}

        raise HTTPException(status_code=404, detail="No recent shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving shows from the database",
        ) from None


@router.get(
    "/repeats",
    summary="Retrieve Information for All Repeat Shows",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("/repeats", include_in_schema=False)
async def get_repeats():
    """Retrieve all Repeat Shows.

    Returned data: Show ID, date, Best Of flag, Repeat flag and  NPR.org
    show url
    """
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_all_repeats()
        if show_info:
            return {"shows": show_info}

        raise HTTPException(status_code=404, detail="No Repeat shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve Repeat shows from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving Repeat shows from the database",
        ) from None


@router.get(
    "/repeat-best-ofs",
    summary="Retrieve Information for All Repeat Best Of Shows",
    response_model=ModelsShows,
    tags=["Shows"],
)
@router.head("/repeat-best-ofs", include_in_schema=False)
async def get_repeat_best_ofs():
    """Retrieve all Repeat Best Of Shows.

    Returned data: Show ID, date, Best Of flag, Repeat flag and  NPR.org
    show url
    """
    try:
        show = Show(database_connection=_database_connection)
        show_info = show.retrieve_all_repeat_best_ofs()
        if show_info:
            return {"shows": show_info}

        raise HTTPException(status_code=404, detail="No Repeat Best Of shows found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve Repeat Best Of shows from the database",
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving Repeat Best Of shows "
            "from the database",
        ) from None
