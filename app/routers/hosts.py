# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Hosts endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.host import Host

from app.config import API_VERSION, load_config
from app.models.hosts import Host as ModelsHost
from app.models.hosts import HostDetails as ModelsHostDetails
from app.models.hosts import HostID as ModelsHostID
from app.models.hosts import Hosts as ModelsHosts
from app.models.hosts import HostsDetails as ModelsHostsDetails
from app.models.hosts import HostSlug as ModelsHostSlug
from app.models.messages import MessageDetails

router = APIRouter(prefix=f"/v{API_VERSION}/hosts")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Hosts",
    response_model=ModelsHosts,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("", include_in_schema=False)
async def get_hosts():
    """Retrieve All Hosts.

    Returned data: Host ID, name, slug string and gender.

    Hosts are sorted by host name.
    """
    try:
        host = Host(database_connection=_database_connection)
        hosts = host.retrieve_all()
        if hosts:
            return {"hosts": hosts}

        return JSONResponse(status_code=404, content={"detail": "No hosts found"})
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve hosts from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving hosts from the database"
            },
        )


@router.get(
    "/id/{host_id}",
    summary="Retrieve Information by Host ID",
    response_model=ModelsHost,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/id/{host_id}", include_in_schema=False)
async def get_host_by_id(
    host_id: Annotated[int, Path(title="The ID of the host to get", ge=0, lt=2**31)],
):
    """Retrieve a Host by Host ID.

    Returned data: Host ID, name, slug string and gender.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_info = host.retrieve_by_id(host_id)
        if host_info:
            return host_info

        return JSONResponse(
            status_code=404, content={"detail": f"Host ID {host_id} not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": f"Host ID {host_id} not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve host information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve host information"
            },
        )


@router.get(
    "/slug/{host_slug}",
    summary="Retrieve Information by Host Slug String",
    response_model=ModelsHost,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/slug/{host_slug}", include_in_schema=False)
async def get_host_by_slug(
    host_slug: Annotated[str, Path(title="The slug string of the host to get")],
):
    """Retrieve a Host by Host Slug String.

    Returned data: Host ID, name, slug string and gender.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_info = host.retrieve_by_slug(host_slug)
        if host_info:
            return host_info

        return JSONResponse(
            status_code=404,
            content={"detail": f"Host slug string {host_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Host slug string {host_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve host information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve host information"
            },
        )


@router.get(
    "/details",
    summary="Retrieve Information and Appearances for All Hosts",
    response_model=ModelsHostsDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/details", include_in_schema=False)
async def get_hosts_details():
    """Retrieve Details for All Hosts.

    Returned data: Host ID, name, slug string, gender, and appearances.

    Hosts are sorted by host name. Appearances are sorted by date.
    """
    try:
        host = Host(database_connection=_database_connection)
        hosts = host.retrieve_all_details()
        if hosts:
            return {"hosts": hosts}

        return JSONResponse(status_code=404, content={"detail": "No hosts found"})
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve hosts from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving hosts from the database"
            },
        )


@router.get(
    "/details/id/{host_id}",
    summary="Retrieve Information and Appearances by Host ID",
    response_model=ModelsHostDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/details/id/{host_id}", include_in_schema=False)
async def get_host_details_by_id(
    host_id: Annotated[int, Path(title="The ID of the host to get", ge=0, lt=2**31)],
):
    """Retrieve Details for a Host by Host ID.

    Returned data: Host ID, name, slug string, gender, and appearances.

    Appearances are sorted by date.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_details = host.retrieve_details_by_id(host_id)
        if host_details:
            return host_details

        return JSONResponse(
            status_code=404, content={"detail": f"Host ID {host_id} not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": f"Host ID {host_id} not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve host information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve host information"
            },
        )


@router.get(
    "/details/random",
    summary="Retrieve Information and Appearances for a Random Host",
    response_model=ModelsHostDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/details/random", include_in_schema=False)
async def get_random_host_details():
    """Retrieve a Random Host.

    Returned data: Host ID, name, slug string, gender, and appearances.

    Appearances are sorted by date.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_details = host.retrieve_random_details()
        if host_details:
            return host_details

        return JSONResponse(
            status_code=404, content={"detail": "Random Host not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Host not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve host information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve host information"
            },
        )


@router.get(
    "/details/slug/{host_slug}",
    summary="Retrieve Information and Appearances by Host by Slug String",
    response_model=ModelsHostDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/details/slug/{host_slug}", include_in_schema=False)
async def get_host_details_by_slug(
    host_slug: Annotated[str, Path(title="The slug string of the host to get")],
):
    """Retrieve Details for a Host by Host Slug String.

    Returned data: Host ID, name, slug string, gender, and appearances.

    Appearances are sorted by date.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_details = host.retrieve_details_by_slug(host_slug)
        if host_details:
            return host_details

        return JSONResponse(
            status_code=404,
            content={"detail": f"Host slug string {host_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Host slug string {host_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve host information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve host information"
            },
        )


@router.get(
    "/random",
    summary="Retrieve Information for a Random Host",
    response_model=ModelsHost,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/random", include_in_schema=False)
async def get_random_host():
    """Retrieve a Random Host.

    Returned data: Host ID, name, slug string and gender.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_info = host.retrieve_random()
        if host_info:
            return host_info

        return JSONResponse(
            status_code=404, content={"detail": "Random Host not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Host not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve host information"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve host information"
            },
        )


@router.get(
    "/random/id",
    summary="Retrieve a Random Host ID",
    response_model=ModelsHostID,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/random/id", include_in_schema=False)
async def get_random_host_id():
    """Retrieve a Random Host ID.

    Returned data: Host ID.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_id = host.retrieve_random_id()
        if host_id:
            return {"id": host_id}

        return JSONResponse(
            status_code=404, content={"detail": "Random Host ID not returned"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Host ID not returned"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500, content={"detail": "Unable to retrieve a random host ID"}
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a random host ID"
            },
        )


@router.get(
    "/random/slug",
    summary="Retrieve a Random Host Slug String",
    response_model=ModelsHostSlug,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Hosts"],
)
@router.head("/random/slug", include_in_schema=False)
async def get_random_host_slug():
    """Retrieve a Random Host Slug String.

    Returned data: Host slug string.
    """
    try:
        host = Host(database_connection=_database_connection)
        host_slug = host.retrieve_random_slug()
        if host_slug:
            return {"slug": host_slug}

        return JSONResponse(
            status_code=404, content={"detail": "Random Host slug string not returned"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Host slug string not returned"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve a random host slug string"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a random host slug string"
            },
        )
