# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Locations endpoints"""

from app.config import API_VERSION, load_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import constr, PositiveInt
from wwdtm.location import details, info
from app.models.locations import (Location, Locations,
                                  LocationDetails, LocationsDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/locations"
)
_app_config = load_config()
_database_connection = mysql.connector.connect(**_app_config)
_database_connection.autocommit = True

#region Routes
@router.get("/", summary="Retrieve Information for All Locations",
            response_model=Locations, tags=["Locations"])
async def get_locations():
    """Retrieve an array of Location objects, each containing:
    Location ID, city, state, venue, and slug string.

    Results are sorted by: city, state, venue name."""
    try:
        _database_connection.reconnect()
        locations = info.retrieve_all(_database_connection)
        if not locations:
            raise HTTPException(status_code=404, detail="No locations found")
        else:
            return {"locations": locations}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve locations from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "locations from the database")


@router.get("/recordings",
            summary="Retrieve Information and Recordings for All Locations",
            response_model=LocationsDetails, tags=["Locations"])
async def get_locations_details():
    """Retrieve an array of Location objects, each containing:
    Location ID, city, state, venue, slug string, and an array of
    recordings.

    Results are sorted by: city, state, venue name."""
    try:
        _database_connection.reconnect()
        locations = details.retrieve_all_recordings(_database_connection)
        if not locations:
            raise HTTPException(status_code=404, detail="No locations found")
        else:
            return {"locations": locations}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve locations from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "locations from the database")


@router.get("/{location_id}",
            summary="Retrieve Information by Location ID",
            response_model=Location, tags=["Locations"])
async def get_location_by_id(location_id: PositiveInt):
    """Retrieve a Location object, based on Location ID, containing:
    Location ID, city, state, venue, and slug string."""
    try:
        _database_connection.reconnect()
        location_info = info.retrieve_by_id(location_id, _database_connection)
        if not location_info:
            raise HTTPException(status_code=404,
                                detail=f"Location ID {location_id} not found")
        else:
            return location_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")


@router.get("/{location_id}/recordings",
            summary="Retrieve Information and Recordings by Location ID",
            response_model=LocationDetails, tags=["Locations"])
async def get_location_recordings_by_id(location_id: PositiveInt):
    """Retrieve a Location object, based on Location ID, containing:
    Location ID, city, state, venue, slug string, and an array of
    recordings.

    Recordings are sorted by show date."""
    try:
        _database_connection.reconnect()
        location_recordings = details.retrieve_recordings_by_id(location_id,
                                                                _database_connection)
        if not location_recordings:
            raise HTTPException(status_code=404,
                                detail=f"Location ID {location_id} not found")
        else:
            return location_recordings
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")


@router.get("/slug/{location_slug}",
            summary="Retrieve Information by Location Slug String",
            response_model=Location, tags=["Locations"])
async def get_location_by_slug(location_slug: constr(strip_whitespace = True)):
    """Retrieve a location object, based on Location slug string,
    containing: Location ID, city, state, venue, and slug string."""
    try:
        _database_connection.reconnect()
        location_info = info.retrieve_by_slug(location_slug, _database_connection)
        if not location_info:
            raise HTTPException(status_code=404,
                                detail=f"Location slug string {location_slug} not found")
        else:
            return location_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")


@router.get("/slug/{location_slug}/recordings",
            summary="Retrieve Information and Recordings by Location Slug String",
            response_model=LocationDetails, tags=["Locations"])
async def get_location_recordings_by_slug(location_slug: constr(strip_whitespace = True)):
    """Retrieve a Location object, based on Location slug string,
    containing: Location ID, city, state, venue, slug string, and an
    array of recordings.

    Recordings are sorted by show date."""
    try:
        _database_connection.reconnect()
        location_details = details.retrieve_recordings_by_slug(location_slug,
                                                               _database_connection)
        if not location_details:
            raise HTTPException(status_code=404,
                                detail=f"Location ID {location_slug} not found")
        else:
            return location_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve location information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve location information")

#endregion
