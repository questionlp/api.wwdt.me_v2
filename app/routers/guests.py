# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Not My Job Guests endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.guest import Guest

from app.config import API_VERSION, load_config
from app.models.guests import Guest as ModelsGuest
from app.models.guests import GuestDetails as ModelsGuestDetails
from app.models.guests import GuestID as ModelsGuestID
from app.models.guests import Guests as ModelsGuests
from app.models.guests import GuestsDetails as ModelsGuestsDetails
from app.models.guests import GuestSlug as ModelsGuestSlug
from app.models.messages import MessageDetails

router = APIRouter(prefix=f"/v{API_VERSION}/guests")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Not My Job Guests",
    response_model=ModelsGuests,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
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

        return JSONResponse(status_code=404, content={"detail": "No guests found"})
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve guests from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving guests from the database"
            },
        )


@router.get(
    "/id/{guest_id}",
    summary="Retrieve Information by Not My Job Guest ID",
    response_model=ModelsGuest,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/id/{guest_id}", include_in_schema=False)
async def get_guest_by_id(
    guest_id: Annotated[int, Path(title="The ID of the guest to get", ge=0, lt=2**31)],
):
    """Retrieve a Not My Job Guest by Guest ID.

    Returned data: Guest ID, name and slug string.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_info = guest.retrieve_by_id(guest_id)
        if guest_info:
            return guest_info

        return JSONResponse(
            status_code=404, content={"detail": f"Guest ID {guest_id} not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": f"Guest ID {guest_id} not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve guest information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve guest information"
            },
        )


@router.get(
    "/slug/{guest_slug}",
    summary="Retrieve Information by Guest Slug String",
    response_model=ModelsGuest,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/slug/{guest_slug}", include_in_schema=False)
async def get_guest_by_slug(
    guest_slug: Annotated[str, Path(title="The slug string of the guest to get")],
):
    """Retrieve a Not My Job Guest by Guest Slug String.

    Returned data: Guest ID, name and slug string.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_info = guest.retrieve_by_slug(guest_slug.strip())
        if guest_info:
            return guest_info

        return JSONResponse(
            status_code=404,
            content={"detail": f"Guest slug string {guest_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Guest slug string {guest_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve guest information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve guest information"
            },
        )


@router.get(
    "/details",
    summary="Retrieve Information and Appearances for All Not My Job Guests",
    response_model=ModelsGuestsDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
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

        return JSONResponse(status_code=404, content={"detail": "No guests found"})
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve guests from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving guests from the database"
            },
        )


@router.get(
    "/details/id/{guest_id}",
    summary="Retrieve Information and Appearances by Not My Job Guest ID",
    response_model=ModelsGuestDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/details/id/{guest_id}", include_in_schema=False)
async def get_guest_details_by_id(
    guest_id: Annotated[int, Path(title="The ID of the guest to get", ge=0, lt=2**31)],
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

        return JSONResponse(
            status_code=404, content={"detail": f"Guest ID {guest_id} not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": f"Guest ID {guest_id} not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve guest information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve guest information"
            },
        )


@router.get(
    "/details/random",
    summary="Retrieve Information and Appearances for a Random Not My Job Guest",
    response_model=ModelsGuestDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/details/random", include_in_schema=False)
async def get_random_guest_details():
    """Retrieve a Random Not My Job Guest.

    Returned data: Guest ID, name, slug string, appearances and scores.

    Appearances are sorted by date.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_details = guest.retrieve_random_details()
        if guest_details:
            return guest_details

        return JSONResponse(
            status_code=404, content={"detail": "Random Guest not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Guest not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve guest information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve guest information"
            },
        )


@router.get(
    "/details/slug/{guest_slug}",
    summary="Retrieve Information and Appearances by Guest Slug String",
    response_model=ModelsGuestDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/details/slug/{guest_slug}", include_in_schema=False)
async def get_guest_details_by_slug(
    guest_slug: Annotated[str, Path(title="The slug string of the guest to get")],
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

        return JSONResponse(
            status_code=404,
            content={"detail": f"Guest slug string {guest_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Guest slug string {guest_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve guest information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve guest information"
            },
        )


@router.get(
    "/random",
    summary="Retrieve Information for a Random Not My Job Guest",
    response_model=ModelsGuest,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/random", include_in_schema=False)
async def get_random_guest():
    """Retrieve a Random Not My Job Guest.

    Returned data: Guest ID, name and slug string.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_info = guest.retrieve_random()
        if guest_info:
            return guest_info

        return JSONResponse(
            status_code=404, content={"detail": "Random Guest not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Guest not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve guest information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve guest information"
            },
        )


@router.get(
    "/random/id",
    summary="Retrieve a Random Not My Job Guest ID",
    response_model=ModelsGuestID,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/random/id", include_in_schema=False)
async def get_random_guest_id():
    """Retrieve a Random Not My Job Guest ID.

    Returned data: Guest ID.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_id = guest.retrieve_random_id()
        if guest_id:
            return {"id": guest_id}

        return JSONResponse(
            status_code=404, content={"detail": "Random Guest ID not returned"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Guest ID not returned"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve a random guest ID"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a random guest ID"
            },
        )


@router.get(
    "/random/slug",
    summary="Retrieve a Random Not My Job Guest Slug String",
    response_model=ModelsGuestSlug,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Guests"],
)
@router.head("/random/slug", include_in_schema=False)
async def get_random_guest_slug():
    """Retrieve a Random Not My Job Guest Slug String.

    Returned data: Guest slug string.
    """
    try:
        guest = Guest(database_connection=_database_connection)
        guest_slug = guest.retrieve_random_slug()
        if guest_slug:
            return {"slug": guest_slug}

        return JSONResponse(
            status_code=404, content={"detail": "Random Guest slug string not returned"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Guest slug string not returned"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve a random guest slug string"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a random guest slug string"
            },
        )
