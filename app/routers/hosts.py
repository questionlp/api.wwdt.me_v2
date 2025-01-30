# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Hosts endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, HTTPException, Path
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.host import Host

from app.config import API_VERSION, load_config
from app.models.hosts import Host as ModelsHost
from app.models.hosts import HostDetails as ModelsHostDetails
from app.models.hosts import Hosts as ModelsHosts
from app.models.hosts import HostsDetails as ModelsHostsDetails

router = APIRouter(prefix=f"/v{API_VERSION}/hosts")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Hosts",
    response_model=ModelsHosts,
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

        raise HTTPException(status_code=404, detail="No hosts found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve hosts from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving hosts from the database",
        ) from None


@router.get(
    "/id/{host_id}",
    summary="Retrieve Information by Host ID",
    response_model=ModelsHost,
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

        raise HTTPException(status_code=404, detail=f"Host ID {host_id} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Host ID {host_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve host information",
        ) from None


@router.get(
    "/slug/{host_slug}",
    summary="Retrieve Information by Host Slug String",
    response_model=ModelsHost,
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

        raise HTTPException(
            status_code=404, detail=f"Host slug string {host_slug} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Host slug string {host_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve host information",
        ) from None


@router.get(
    "/details",
    summary="Retrieve Information and Appearances for All Hosts",
    response_model=ModelsHostsDetails,
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

        raise HTTPException(status_code=404, detail="No hosts found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve hosts from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving hosts from the database",
        ) from None


@router.get(
    "/details/id/{host_id}",
    summary="Retrieve Information and Appearances by Host ID",
    response_model=ModelsHostDetails,
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

        raise HTTPException(status_code=404, detail=f"Host ID {host_id} not found")
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Host ID {host_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve host information",
        ) from None


@router.get(
    "/details/slug/{host_slug}",
    summary="Retrieve Information and Appearances by Host by Slug String",
    response_model=ModelsHostDetails,
    tags=["Hosts"],
)
@router.head("/details/slug/{host_slug}", include_in_schema=False)
async def get_host_details_by_slug(
    host_slug: Annotated[str, Path(title="The slug string of the guest to get")],
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

        raise HTTPException(
            status_code=404, detail=f"Host slug string {host_slug} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Host slug string {host_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve host information",
        ) from None
