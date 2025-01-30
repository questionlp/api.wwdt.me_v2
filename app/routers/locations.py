# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Locations endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, HTTPException, Path
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.location import Location

from app.config import API_VERSION, load_config
from app.models.locations import Location as ModelsLocation
from app.models.locations import LocationDetails as ModelsLocationDetails
from app.models.locations import Locations as ModelsLocations
from app.models.locations import LocationsDetails as ModelsLocationsDetails

router = APIRouter(prefix=f"/v{API_VERSION}/locations")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Locations",
    response_model=ModelsLocations,
    tags=["Locations"],
)
@router.head("", include_in_schema=False)
async def get_locations():
    """Retrieve All Show Locations.

    Returned data: Location ID, city, state, venue and slug string.

    Locations are sorted by venue name, city, and state.
    """
    try:
        location = Location(database_connection=_database_connection)
        locations = location.retrieve_all(sort_by_venue=True)
        if locations:
            return {"locations": locations}

        raise HTTPException(status_code=404, detail="No locations found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve locations from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving locations from the database",
        ) from None


@router.get(
    "/id/{location_id}",
    summary="Retrieve Information by Location ID",
    response_model=ModelsLocation,
    tags=["Locations"],
)
@router.head("/id/{location_id}", include_in_schema=False)
async def get_location_by_id(
    location_id: Annotated[
        int, Path(title="The ID of the location to get", ge=0, lt=2**31)
    ],
):
    """Retrieve a Show Location by Location ID.

    Returned data: Location ID, city, state, venue and slug string.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_info = location.retrieve_by_id(location_id)
        if location_info:
            return location_info

        raise HTTPException(
            status_code=404, detail=f"Location ID {location_id} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Location ID {location_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve location information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve location information",
        ) from None


@router.get(
    "/slug/{location_slug}",
    summary="Retrieve Information by Location Slug String",
    response_model=ModelsLocation,
    tags=["Locations"],
)
@router.head("/slug/{location_slug}", include_in_schema=False)
async def get_location_by_slug(
    location_slug: Annotated[str, Path(title="The slug string of the location to get")],
):
    """Retrieve a Show Location by Location Slug String.

    Returned data: Location ID, city, state, venue and slug string.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_info = location.retrieve_by_slug(location_slug.strip())
        if location_info:
            return location_info

        raise HTTPException(
            status_code=404,
            detail=f"Location slug string {location_slug} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Location slug string {location_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve location information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve location information",
        ) from None


@router.get(
    "/recordings",
    summary="Retrieve Information and Recordings for All Locations",
    response_model=ModelsLocationsDetails,
    tags=["Locations"],
)
@router.head("/recordings", include_in_schema=False)
async def get_locations_details():
    """Retrieve Details for All Show Locations.

    Returned data: Location ID, city, state, venue, slug string and
    recordings.

    Locations are sorted by venue name, city, and state. Recordings are
    sorted by show date.
    """
    try:
        location = Location(database_connection=_database_connection)
        locations = location.retrieve_all_details(sort_by_venue=True)
        if locations:
            return {"locations": locations}

        raise HTTPException(status_code=404, detail="No locations found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve locations from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving locations from the database",
        ) from None


@router.get(
    "/recordings/id/{location_id}",
    summary="Retrieve Information and Recordings by Location ID",
    response_model=ModelsLocationDetails,
    tags=["Locations"],
)
@router.head("/recordings/id/{location_id}", include_in_schema=False)
async def get_location_recordings_by_id(
    location_id: Annotated[
        int, Path(title="The ID of the location to get", ge=0, lt=2**31)
    ],
):
    """Retrieve Details for a Show Location by Location ID.

    Returned data: Location ID, city, state, venue, slug string and
    recordings.

    Recordings are sorted by show date.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_recordings = location.retrieve_details_by_id(location_id)
        if location_recordings:
            return location_recordings

        raise HTTPException(
            status_code=404, detail=f"Location ID {location_id} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Location ID {location_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve location information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve location information",
        ) from None


@router.get(
    "/recordings/slug/{location_slug}",
    summary="Retrieve Information and Recordings by Location Slug String",
    response_model=ModelsLocationDetails,
    tags=["Locations"],
)
@router.head("/recordings/slug/{location_slug}", include_in_schema=False)
async def get_location_recordings_by_slug(
    location_slug: Annotated[str, Path(title="The slug string of the location to get")],
):
    """Retrieve Details for a Show Location by Location Slug String.

    Returned data: Location ID, city, state, venue, slug string and
    recordings.

    Recordings are sorted by show date.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_details = location.retrieve_details_by_slug(location_slug.strip())
        if location_details:
            return location_details

        raise HTTPException(
            status_code=404,
            detail=f"Location slug string {location_slug} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Location slug string {location_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve location information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve location information",
        ) from None
