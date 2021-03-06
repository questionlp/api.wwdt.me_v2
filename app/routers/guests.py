# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""API routes for Not My Job Guests endpoints"""

from app.config import API_VERSION, load_database_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import conint, constr
from wwdtm.guest import Guest
from app.models.guests import (
    Guest as ModelsGuest,
    Guests as ModelsGuests,
    GuestDetails as ModelsGuestDetails,
    GuestsDetails as ModelsGuestsDetails,
)

router = APIRouter(prefix=f"/v{API_VERSION}/guests")
_database_config = load_database_config()
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Not My Job Guests",
    response_model=ModelsGuests,
    tags=["Guests"],
)
@router.head("", include_in_schema=False)
async def get_guests():
    """Retrieve an array of Not My Job Guest objects, each containing:
    Guest ID, name and slug string.

    Results are sorted by guest name."""
    try:
        guest = Guest(database_connection=_database_connection)
        guests = guest.retrieve_all()
        if not guests:
            raise HTTPException(status_code=404, detail="No guests found")
        else:
            return {"guests": guests}
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guests from the database"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving "
            "guests from the database",
        )


@router.get(
    "/id/{guest_id}",
    summary="Retrieve Information by Not My Job Guest ID",
    response_model=ModelsGuest,
    tags=["Guests"],
)
@router.head("/id/{guest_id}", include_in_schema=False)
async def get_guest_by_id(guest_id: conint(ge=0, lt=2**31)):
    """Retrieve a Not My Job Guest object, based on Guest ID,
    containing: Guest ID, name and slug string."""
    try:
        guest = Guest(database_connection=_database_connection)
        guest_info = guest.retrieve_by_id(guest_id)
        if not guest_info:
            raise HTTPException(
                status_code=404, detail=f"Guest ID {guest_id} not found"
            )
        else:
            return guest_info
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Guest ID {guest_id} not found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve guest information",
        )


@router.get(
    "/slug/{guest_slug}",
    summary="Retrieve Information by Guest Slug String",
    response_model=ModelsGuest,
    tags=["Guests"],
)
@router.head("/slug/{guest_slug}", include_in_schema=False)
async def get_guest_by_slug(guest_slug: constr(strip_whitespace=True)):
    """Retrieve a Not My Job Guest object, based on Guest slug string,
    containing: Guest ID, name and slug string."""
    try:
        guest = Guest(database_connection=_database_connection)
        guest_info = guest.retrieve_by_slug(guest_slug)
        if not guest_info:
            raise HTTPException(
                status_code=404, detail=f"Guest slug string {guest_slug} not found"
            )
        else:
            return guest_info
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Guest slug string {guest_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve guest information",
        )


@router.get(
    "/details",
    summary="Retrieve Information and Appearances for All Not My Job Guests",
    response_model=ModelsGuestsDetails,
    tags=["Guests"],
)
@router.head("/details", include_in_schema=False)
async def get_guests_details():
    """Retrieve an array of Not My Job Guest objects, each containing:
    Guest ID, name, slug string and their appearance details.

    Results are sorted by guest name, with guest apperances sorted
    by show date."""
    try:
        guest = Guest(database_connection=_database_connection)
        guests = guest.retrieve_all_details()
        if not guests:
            raise HTTPException(status_code=404, detail="No guests found")
        else:
            return {"guests": guests}
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guests from the database"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving "
            "guests from the database",
        )


@router.get(
    "/details/id/{guest_id}",
    summary="Retrieve Information and Appearances by Not My Job Guest ID",
    response_model=ModelsGuestDetails,
    tags=["Guests"],
)
@router.head("/details/id/{guest_id}", include_in_schema=False)
async def get_guest_details_by_id(guest_id: conint(ge=0, lt=2**31)):
    """Retrieve a Not My Job Guest object, based on Guest ID,
    containing: Guest ID, name, slug string, and their appearance details.

    Guest appearances are sorted by show date."""
    try:
        guest = Guest(database_connection=_database_connection)
        guest_details = guest.retrieve_details_by_id(guest_id)
        if not guest_details:
            raise HTTPException(
                status_code=404, detail=f"Guest ID {guest_id} not found"
            )
        else:
            return guest_details
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Guest ID {guest_id} not found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve guest information",
        )


@router.get(
    "/details/slug/{guest_slug}",
    summary="Retrieve Information and Appearances by Guest Slug String",
    response_model=ModelsGuestDetails,
    tags=["Guests"],
)
@router.head("/details/slug/{guest_slug}", include_in_schema=False)
async def get_guest_details_by_slug(guest_slug: constr(strip_whitespace=True)):
    """Retrieve a Not My Job Guest object, based on Guest slug string,
    containing: Guest ID, name, slug string, and their appearance details.

    Guest appearances are sorted by show date."""
    try:
        guest = Guest(database_connection=_database_connection)
        guest_details = guest.retrieve_details_by_slug(guest_slug)
        if not guest_details:
            raise HTTPException(
                status_code=404, detail=f"Guest slug string {guest_slug} not found"
            )
        else:
            return guest_details
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Guest slug string {guest_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve guest information",
        )
