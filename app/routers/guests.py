# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI guests router module for api.wwdt.me"""

from app.dependencies import API_VERSION, load_config
from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import BaseModel
from wwdtm.guest import details, info

#region Models
class Guest(BaseModel):
    id: int
    name: str
    slug: str

class Guests(BaseModel):
    guests: List[Guest]

class GuestAppearanceCounts(BaseModel):
    regular_shows: int
    all_shows: int

class GuestAppearance(BaseModel):
    show_id: int
    date: str
    best_of: bool
    repeat_show: bool
    score: Optional[int]
    score_exception: bool

class GuestAppearances(BaseModel):
    count: Union[GuestAppearanceCounts, int]
    shows: Optional[List[GuestAppearance]]

class GuestDetails(Guest):
    appearances: Optional[GuestAppearances]

class GuestsDetails(BaseModel):
    guests: List[GuestDetails]

#endregion

router = APIRouter(
    prefix=f"/v{API_VERSION}/guests"
)
_app_config = load_config()
_database_connection = mysql.connector.connect(**_app_config)
_database_connection.autocommit = True

#region Routes
@router.get("/",
            summary="Get Information for All Not My Job Guests",
            response_model=Guests, tags=["Guests"])
async def get_guests():
    """Retrieve a list containing information all Not My Job Guests"""
    try:
        _database_connection.reconnect()
        guests = info.retrieve_all(_database_connection)
        if not guests:
            raise HTTPException(status_code=404, detail="No guests found")
        else:
            return {"guests": guests}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve guests from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "guests from the database")


@router.get("/details",
            summary="Get Information and Appearances for All Not My Job Guests",
            response_model=GuestsDetails, tags=["Guests"])
async def get_guests_details():
    """Retrieve a list containing information and appearances for all
    Not My Job Guests"""
    try:
        _database_connection.reconnect()
        guests = details.retrieve_all(_database_connection)
        if not guests:
            raise HTTPException(status_code=404, detail="No guests found")
        else:
            return {"guests": guests}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve guests from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "guests from the database")


@router.get("/{guest_id}",
            summary="Get Information by Not My Job Guest ID",
            response_model=Guest, tags=["Guests"])
async def get_guest_by_id(guest_id: int):
    """Retrieve information for a given Not My Job Guest ID"""
    try:
        _database_connection.reconnect()
        guest_info = info.retrieve_by_id(guest_id, _database_connection)
        if not guest_info:
            raise HTTPException(status_code=404,
                                detail=f"Guest ID {guest_id} not found")
        else:
            return guest_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve guest information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve guest information")


@router.get("/{guest_id}/details",
            summary="Get Information and Appearances by Not My Job Guest ID",
            response_model=GuestDetails, tags=["Guests"])
async def get_guest_details_by_id(guest_id: int):
    """Retrieve information and appearances for a given Not My Job Guest ID"""
    try:
        _database_connection.reconnect()
        guest_details = details.retrieve_by_id(guest_id, _database_connection)
        if not guest_details:
            raise HTTPException(status_code=404,
                                detail=f"Guest ID {guest_id} not found")
        else:
            return guest_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve guest information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve guest information")


@router.get("/slug/{guest_slug}",
            summary="Get Information by Guest Slug String",
            response_model=Guest, tags=["Guests"])
async def get_guest_by_slug(guest_slug: str):
    """Retrieve information for a given Not My Job Guest slug string"""
    try:
        _database_connection.reconnect()
        guest_info = info.retrieve_by_slug(guest_slug, _database_connection)
        if not guest_info:
            raise HTTPException(status_code=404,
                                detail=f"Guest slug string {guest_slug} not found")
        else:
            return guest_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve guest information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve guest information")


@router.get("/slug/{guest_slug}/details",
            summary="Get Information and Appearances by Guest Slug String",
            response_model=GuestDetails, tags=["Guests"])
async def get_guest_details_by_slug(guest_slug: str):
    """Retrieve information and appearances for a given Not My Job
    Guest slug string"""
    try:
        _database_connection.reconnect()
        guest_details = details.retrieve_by_slug(guest_slug, _database_connection)
        if not guest_details:
            raise HTTPException(status_code=404,
                                detail=f"Guest ID {guest_slug} not found")
        else:
            return guest_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve guest information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve guest information")

#endregion
