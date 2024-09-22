# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Not My Job Guests endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, HTTPException, Path
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.guest import Guest

from app.config import API_VERSION, load_config
from app.models.guests import Guest as ModelsGuest
from app.models.guests import GuestDetails as ModelsGuestDetails
from app.models.guests import Guests as ModelsGuests
from app.models.guests import GuestsDetails as ModelsGuestsDetails

router = APIRouter(prefix=f"/v{API_VERSION}/guests")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Not My Job Guests",
    response_model=ModelsGuests,
    tags=["Guests"],
)
@router.head("", include_in_schema=False)
async def get_guests():
    """Retrieve All Not My Job Guests.

    Returned data: Guest ID, name and slug string.

    Guests are sorted by guest name.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guests = guest.retrieve_all()
        if guests:
            return {"guests": guests}

        raise HTTPException(status_code=404, detail="No guests found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guests from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving guests from the database",
        ) from None


@router.get(
    "/id/{guest_id}",
    summary="Retrieve Information by Not My Job Guest ID",
    response_model=ModelsGuest,
    tags=["Guests"],
)
@router.head("/id/{guest_id}", include_in_schema=False)
async def get_guest_by_id(
    guest_id: Annotated[int, Path(title="The ID of the guest to get", ge=0, lt=2**31)]
):
    """Retrieve a Not My Job Guest by Guest ID.

    Returned data: Guest ID, name and slug string.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_info = guest.retrieve_by_id(guest_id)
        if guest_info:
            return guest_info

        raise HTTPException(status_code=404, detail=f"Guest ID {guest_id} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Guest ID {guest_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve guest information",
        ) from None


@router.get(
    "/slug/{guest_slug}",
    summary="Retrieve Information by Guest Slug String",
    response_model=ModelsGuest,
    tags=["Guests"],
)
@router.head("/slug/{guest_slug}", include_in_schema=False)
async def get_guest_by_slug(
    guest_slug: Annotated[str, Path(title="The slug string of the guest to get")]
):
    """Retrieve a Not My Job Guest by Guest Slug String.

    Returned data: Guest ID, name and slug string.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_info = guest.retrieve_by_slug(guest_slug.strip())
        if guest_info:
            return guest_info

        raise HTTPException(
            status_code=404, detail=f"Guest slug string {guest_slug} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Guest slug string {guest_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve guest information",
        ) from None


@router.get(
    "/details",
    summary="Retrieve Information and Appearances for All Not My Job Guests",
    response_model=ModelsGuestsDetails,
    tags=["Guests"],
)
@router.head("/details", include_in_schema=False)
async def get_guests_details():
    """Retrieve Details for All Not My Job Guests.

    Returned data: Guest ID, name, slug string, appearances and scores.

    Guests are sorted by guest name. Appearances are sorted by date.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guests = guest.retrieve_all_details()
        if guests:
            return {"guests": guests}

        raise HTTPException(status_code=404, detail="No guests found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guests from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving guests from the database",
        ) from None


@router.get(
    "/details/id/{guest_id}",
    summary="Retrieve Information and Appearances by Not My Job Guest ID",
    response_model=ModelsGuestDetails,
    tags=["Guests"],
)
@router.head("/details/id/{guest_id}", include_in_schema=False)
async def get_guest_details_by_id(
    guest_id: Annotated[int, Path(title="The ID of the guest to get", ge=0, lt=2**31)]
):
    """Retrieve Details for a Not My Job Guest by Guest ID.

    Returned data: Guest ID, name, slug string, appearances and scores.

    Appearances are sorted by date.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_details = guest.retrieve_details_by_id(guest_id)
        if guest_details:
            return guest_details

        raise HTTPException(status_code=404, detail=f"Guest ID {guest_id} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Guest ID {guest_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve guest information",
        ) from None


@router.get(
    "/details/slug/{guest_slug}",
    summary="Retrieve Information and Appearances by Guest Slug String",
    response_model=ModelsGuestDetails,
    tags=["Guests"],
)
@router.head("/details/slug/{guest_slug}", include_in_schema=False)
async def get_guest_details_by_slug(
    guest_slug: Annotated[str, Path(title="The slug string of the guest to get")]
):
    """Retrieve Details for a Not My Job Guest by Guest Slug String.

    Returned data: Guest ID, name, slug string, appearances and scores.

    Appearances are sorted by date.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_details = guest.retrieve_details_by_slug(guest_slug.strip())
        if guest_details:
            return guest_details

        raise HTTPException(
            status_code=404, detail=f"Guest slug string {guest_slug} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Guest slug string {guest_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve guest information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve guest information",
        ) from None
