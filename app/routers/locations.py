# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Locations endpoints"""

from app.config import API_VERSION, load_database_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import conint, constr
from wwdtm.location import Location
from app.models.locations import (Location as ModelsLocation,
                                  Locations as ModelsLocations,
                                  LocationDetails as ModelsLocationDetails,
                                  LocationsDetails as ModelsLocationsDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/locations"
)
_database_config = load_database_config()
_database_connection = mysql.connector.connect(**_database_config)
_database_connection.autocommit = True


# region Routes
@router.get("",
            summary="Retrieve Information for All Locations",
            response_model=ModelsLocations,
            tags=["Locations"])
@router.head("",
             include_in_schema=False)
async def get_locations():
    """Retrieve an array of Location objects, each containing:
    Location ID, city, state, venue, and slug string.

    Results are sorted by: city, state, venue name."""
    try:
        location = Location(database_connection=_database_connection)
        locations = location.retrieve_all()
        if not locations:
            raise HTTPException(status_code=404,
                                detail="No locations found")
        else:
            return {"locations": locations}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve locations from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "locations from the database")


@router.get("/id/{location_id}",
            summary="Retrieve Information by Location ID",
            response_model=ModelsLocation,
            tags=["Locations"])
@router.head("/id/{location_id}",
             include_in_schema=False)
async def get_location_by_id(location_id: conint(ge=0, lt=2**31)):
    """Retrieve a Location object, based on Location ID, containing:
    Location ID, city, state, venue, and slug string."""
    try:
        location = Location(database_connection=_database_connection)
        location_info = location.retrieve_by_id(location_id)
        if not location_info:
            raise HTTPException(status_code=404,
                                detail=f"Location ID {location_id} not found")
        else:
            return location_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Location ID {location_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")


@router.get("/slug/{location_slug}",
            summary="Retrieve Information by Location Slug String",
            response_model=ModelsLocation,
            tags=["Locations"])
@router.head("/slug/{location_slug}",
             include_in_schema=False)
async def get_location_by_slug(location_slug: constr(strip_whitespace=True)):
    """Retrieve a location object, based on Location slug string,
    containing: Location ID, city, state, venue, and slug string."""
    try:
        location = Location(database_connection=_database_connection)
        location_info = location.retrieve_by_slug(location_slug)
        if not location_info:
            raise HTTPException(status_code=404,
                                detail=f"Location slug string {location_slug} not found")
        else:
            return location_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Location slug string {location_slug} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")


@router.get("/recordings",
            summary="Retrieve Information and Recordings for All Locations",
            response_model=ModelsLocationsDetails,
            tags=["Locations"])
@router.head("/recordings",
             include_in_schema=False)
async def get_locations_details():
    """Retrieve an array of Location objects, each containing:
    Location ID, city, state, venue, slug string, and an array of
    recordings.

    Results are sorted by: city, state, venue name."""
    try:
        location = Location(database_connection=_database_connection)
        locations = location.retrieve_all_details()
        if not locations:
            raise HTTPException(status_code=404,
                                detail="No locations found")
        else:
            return {"locations": locations}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve locations from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "locations from the database")


@router.get("/recordings/id/{location_id}",
            summary="Retrieve Information and Recordings by Location ID",
            response_model=ModelsLocationDetails,
            tags=["Locations"])
@router.head("/recordings/id/{location_id}",
             include_in_schema=False)
async def get_location_recordings_by_id(location_id: conint(ge=0, lt=2**31)):
    """Retrieve a Location object, based on Location ID, containing:
    Location ID, city, state, venue, slug string, and an array of
    recordings.

    Recordings are sorted by show date."""
    try:
        location = Location(database_connection=_database_connection)
        location_recordings = location.retrieve_details_by_id(location_id)
        if not location_recordings:
            raise HTTPException(status_code=404,
                                detail=f"Location ID {location_id} not found")
        else:
            return location_recordings
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Location ID {location_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")


@router.get("/recordings/slug/{location_slug}",
            summary="Retrieve Information and Recordings by Location Slug String",
            response_model=ModelsLocationDetails,
            tags=["Locations"])
@router.head("/recordings/slug/{location_slug}",
             include_in_schema=False)
async def get_location_recordings_by_slug(location_slug: constr(strip_whitespace=True)):
    """Retrieve a Location object, based on Location slug string,
    containing: Location ID, city, state, venue, slug string, and an
    array of recordings.

    Recordings are sorted by show date."""
    try:
        location = Location(database_connection=_database_connection)
        location_details = location.retrieve_details_by_slug(location_slug)
        if not location_details:
            raise HTTPException(status_code=404,
                                detail=f"Location slug string {location_slug} not found")
        else:
            return location_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Location slug string {location_slug} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")

# endregion
