# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Locations endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.location import Location

from app.config import API_VERSION, load_config
from app.models.locations import Location as ModelsLocation
from app.models.locations import LocationDetails as ModelsLocationDetails
from app.models.locations import LocationID as ModelsLocationID
from app.models.locations import Locations as ModelsLocations
from app.models.locations import LocationsDetails as ModelsLocationsDetails
from app.models.locations import LocationSlug as ModelsLocationSlug
from app.models.locations import (
    PostalAbbreviationDetails as ModelsPostalAbbreviationDetails,
)
from app.models.locations import PostalAbbreviations as ModelsPostalAbbreviations
from app.models.locations import (
    PostalAbbreviationsDetails as ModelsPostalAbbreviationsDetails,
)
from app.models.messages import MessageDetails

router = APIRouter(prefix=f"/v{API_VERSION}/locations")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Locations",
    response_model=ModelsLocations,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
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

        return JSONResponse(status_code=404, content={"detail": "No locations found"})
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve locations from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving locations from the database"
            },
        )


@router.get(
    "/id/{location_id}",
    summary="Retrieve Information by Location ID",
    response_model=ModelsLocation,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
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

        return JSONResponse(
            status_code=404, content={"detail": f"Location ID {location_id} not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": f"Location ID {location_id} not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve location information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve location information"
            },
        )


@router.get(
    "/slug/{location_slug}",
    summary="Retrieve Information by Location Slug String",
    response_model=ModelsLocation,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
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

        return JSONResponse(
            status_code=404,
            content={"detail": f"Location slug string {location_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Location slug string {location_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve location information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve location information"
            },
        )


@router.get(
    "/recordings",
    summary="Retrieve Information and Recordings for All Locations",
    response_model=ModelsLocationsDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
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

        return JSONResponse(status_code=404, content={"detail": "No locations found"})
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve locations from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving locations from the database"
            },
        )


@router.get(
    "/recordings/id/{location_id}",
    summary="Retrieve Information and Recordings by Location ID",
    response_model=ModelsLocationDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/recordings/id/{location_id}", include_in_schema=False)
async def get_location_details_by_id(
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

        return JSONResponse(
            status_code=404, content={"detail": f"Location ID {location_id} not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": f"Location ID {location_id} not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve location information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve location information"
            },
        )


@router.get(
    "/recordings/random",
    summary="Retrieve Information and Recordings for a Random Location",
    response_model=ModelsLocationDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/recordings/random", include_in_schema=False)
async def get_random_location_details():
    """Retrieve a Random Location.

    Returned data: Location ID, venue, city, state, slug string, and recordings.

    Appearances are sorted by date.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_details = location.retrieve_random_details()
        if location_details:
            return location_details

        return JSONResponse(
            status_code=404, content={"detail": "Random Location not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Location not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve location information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve location information"
            },
        )


@router.get(
    "/recordings/slug/{location_slug}",
    summary="Retrieve Information and Recordings by Location Slug String",
    response_model=ModelsLocationDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/recordings/slug/{location_slug}", include_in_schema=False)
async def get_location_details_by_slug(
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

        return JSONResponse(
            status_code=404,
            content={"detail": f"Location slug string {location_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Location slug string {location_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve location information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve location information"
            },
        )


@router.get(
    "/postal-abbreviations",
    summary="Retrieve Postal Abbreviations",
    response_model=ModelsPostalAbbreviations,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/postal-abbreviations", include_in_schema=False)
async def get_postal_abbreviations() -> list[str]:
    """Retrieve All Postal Abbreviations.

    Returned data: Postal abbreviations for states, provinces and
    territoies.

    Postal abbreviations are sorted alphabetically.
    """
    try:
        location = Location(database_connection=_database_connection)
        abbreviations = location.retrieve_postal_abbreviations()
        if abbreviations:
            return list(abbreviations.keys())

        return JSONResponse(
            status_code=404, content={"detail": "No postal abbreviations found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve postal abbreviations"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve postal abbreviations"
            },
        )


@router.get(
    "/postal-abbreviations/details",
    summary="Retrieve Information for All Postal Abbreviations",
    response_model=ModelsPostalAbbreviationsDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/postal-abbreviations/details", include_in_schema=False)
async def get_postal_abbreviations_details() -> list[dict[str, str]]:
    """Retrieve Details for all All Postal Abbreviations.

    Returned data: Postal abbreviations for states, provinces and
    territoies.

    Postal abbreviations are sorted alphabetically.
    """
    try:
        location = Location(database_connection=_database_connection)
        abbreviations = location.retrieve_postal_abbreviations_list()
        if abbreviations:
            return {"postal_abbreviations": abbreviations}

        return JSONResponse(
            status_code=404, content={"detail": "No postal abbreviations found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve postal abbreviations"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve postal abbreviations"
            },
        )


@router.get(
    "/postal-abbreviations/details/{abbreviation}",
    summary="Retrieve Information for a Postal Abbreviation",
    response_model=ModelsPostalAbbreviationDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/postal-abbreviations/details/{abbreviation}", include_in_schema=False)
async def get_postal_abbreviation_details(
    abbreviation: Annotated[
        str, Path(title="Postal Abbreviation to retrieve information")
    ],
):
    """Retrieve Details for a Postal Abbreviation.

    Returned data: Postal abbreviation, name of the state, province or
    territory, and country.
    """
    try:
        location = Location(database_connection=_database_connection)
        info = location.retrieve_postal_details_by_abbreviation(
            abbreviation=abbreviation
        )
        if info:
            return info

        return JSONResponse(
            status_code=404,
            content={"detail": f"Postal abbreviation {abbreviation} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Postal abbreviation {abbreviation} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve postal abbreviation information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve postal abbreviaton information"
            },
        )


@router.get(
    "/random",
    summary="Retrieve Information for a Random Location",
    response_model=ModelsLocation,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/random", include_in_schema=False)
async def get_random_location():
    """Retrieve a Random Location.

    Returned data: Location ID, venue, city, state and slug string.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_info = location.retrieve_random()
        if location_info:
            return location_info

        return JSONResponse(
            status_code=404, content={"detail": "Random Location not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Location not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve location information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve location information"
            },
        )


@router.get(
    "/random/id",
    summary="Retrieve a Random Location ID",
    response_model=ModelsLocationID,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/random/id", include_in_schema=False)
async def get_random_location_id():
    """Retrieve a Random Location ID.

    Returned data: Location ID.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_id = location.retrieve_random_id()
        if location_id:
            return {"id": location_id}

        return JSONResponse(
            status_code=404, content={"detail": "Random Location ID not returned"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Location ID not returned"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve a random location ID"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a random location ID"
            },
        )


@router.get(
    "/random/slug",
    summary="Retrieve a Random Location Slug String",
    response_model=ModelsLocationSlug,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Locations"],
)
@router.head("/random/slug", include_in_schema=False)
async def get_random_location_slug():
    """Retrieve a Random Location Slug String.

    Returned data: Location slug string.
    """
    try:
        location = Location(database_connection=_database_connection)
        location_slug = location.retrieve_random_slug()
        if location_slug:
            return {"slug": location_slug}

        return JSONResponse(
            status_code=404,
            content={"detail": "Random Location slug string not returned"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": "Random Location slug string not returned"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve a random location slug string"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a location host slug string"
            },
        )
