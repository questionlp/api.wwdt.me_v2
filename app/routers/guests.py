# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Not My Job Guests endpoints"""

from app.dependencies import API_VERSION, load_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import constr, PositiveInt
from wwdtm.guest import details, info
from app.models.guests import (Guest, Guests, GuestDetails, GuestsDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/guests"
)
_app_config = load_config()
_database_connection = mysql.connector.connect(**_app_config)
_database_connection.autocommit = True

#region Routes
@router.get("/",
            summary="Retrieve Information for All Not My Job Guests",
            response_model=Guests, tags=["Guests"])
async def get_guests():
    """Retrieve an array of Not My Job Guest objects, each containing:
    Guest ID, name and slug string.

    Results are sorted by guest name."""
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
            summary="Retrieve Information and Appearances for All Not My Job Guests",
            response_model=GuestsDetails, tags=["Guests"])
async def get_guests_details():
    """Retrieve an array of Not My Job Guest objects, each containing:
    Guest ID, name, slug string and their appearance details.

    Results are sorted by guest name, with guest apperances sorted
    by show date."""
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
            summary="Retrieve Information by Not My Job Guest ID",
            response_model=Guest, tags=["Guests"])
async def get_guest_by_id(guest_id: PositiveInt):
    """Retrieve a Not My Job Guest object, based on Guest ID,
    containing: Guest ID, name and slug string."""
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
            summary="Retrieve Information and Appearances by Not My Job Guest ID",
            response_model=GuestDetails, tags=["Guests"])
async def get_guest_details_by_id(guest_id: PositiveInt):
    """Retrieve a Not My Job Guest object, based on Guest ID,
    containing: Guest ID, name, slug string, and their appearance details.

    Guest appearances are sorted by show date."""
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
            summary="Retrieve Information by Guest Slug String",
            response_model=Guest, tags=["Guests"])
async def get_guest_by_slug(guest_slug: constr(strip_whitespace = True)):
    """Retrieve a Not My Job Guest object, based on Guest slug string,
    containing: Guest ID, name and slug string."""
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
            summary="Retrieve Information and Appearances by Guest Slug String",
            response_model=GuestDetails, tags=["Guests"])
async def get_guest_details_by_slug(guest_slug: constr(strip_whitespace = True)):
    """Retrieve a Not My Job Guest object, based on Guest slug string,
    containing: Guest ID, name, slug string, and their appearance details.

    Guest appearances are sorted by show date."""
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
