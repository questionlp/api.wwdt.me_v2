# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI locations router module for api.wwdt.me"""

from app.dependencies import API_VERSION, load_config
from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import BaseModel
from wwdtm.location import details, info

#region Location Models
class Location(BaseModel):
    id: int
    city: Optional[str]
    state: Optional[str]
    venue: str
    slug: str

class Locations(BaseModel):
    locations: List[Location]

class LocationRecordingCounts(BaseModel):
    regular_shows: Optional[int]
    all_shows: Optional[int]

class LocationRecordingShow(BaseModel):
    show_id: int
    date: str
    best_of: bool
    repeat_show: bool

class LocationRecordings(BaseModel):
    count: Optional[LocationRecordingCounts]
    shows: Optional[List[LocationRecordingShow]]

class LocationDetails(Location):
    recordings: Optional[LocationRecordings]

class LocationsDetails(BaseModel):
    locations: List[LocationDetails]

#endregion

router = APIRouter(
    prefix=f"/v{API_VERSION}/locations"
)
_app_config = load_config()
_database_connection = mysql.connector.connect(**_app_config)
_database_connection.autocommit = True

#region Routes
@router.get("/", summary="Get Information for All Locations",
            response_model=Locations, tags=["Locations"])
async def get_locations():
    """Retrieve a list of all Locations"""
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
            summary="Get Information and Recordings for All Locations",
            response_model=LocationsDetails, tags=["Locations"])
async def get_locations_details():
    """Retrieve a list of all Locations and their recordings"""
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
            summary="Get Information by Location ID",
            response_model=Location, tags=["Locations"])
async def get_location_by_id(location_id: int):
    """Retrieve Location information for a given Location ID"""
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
            summary="Get Information and Recordings by Location ID",
            response_model=LocationDetails, tags=["Locations"])
async def get_location_recordings_by_id(location_id: int):
    """Retrieve Location information and recordings for a given Location
    ID"""
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
            summary="Get Information by Location Slug String",
            response_model=Location, tags=["Locations"])
async def get_location_by_slug(location_slug: str):
    """Retrieve Location information for a given Location slug string"""
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
            summary="Get Information and Recordings by Location Slug String",
            response_model=LocationDetails, tags=["Locations"])
async def get_location_recordings_by_slug(location_slug: str):
    """Retrieve Location information and recordings for a given
    Location slug string"""
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
