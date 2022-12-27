# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""API routes for Hosts endpoints"""

from app.config import API_VERSION, load_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import conint, constr
from wwdtm.host import Host
from app.models.hosts import (
    Host as ModelsHost,
    Hosts as ModelsHosts,
    HostDetails as ModelsHostDetails,
    HostsDetails as ModelsHostsDetails,
)

router = APIRouter(prefix=f"/v{API_VERSION}/hosts")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


# region Routes
@router.get(
    "",
    summary="Retrieve Information for All Hosts",
    response_model=ModelsHosts,
    tags=["Hosts"],
)
@router.head("", include_in_schema=False)
async def get_hosts():
    """Retrieve an array of Host objects, each containing: Host ID,
    name, slug string, and gender.

    Results are sorted by host name."""
    try:
        host = Host(database_connection=_database_connection)
        hosts = host.retrieve_all()
        if not hosts:
            raise HTTPException(status_code=404, detail="No hosts found")
        else:
            return {"hosts": hosts}
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve hosts from the database"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving "
            "hosts from the database",
        )


@router.get(
    "/id/{host_id}",
    summary="Retrieve Information by Host ID",
    response_model=ModelsHost,
    tags=["Hosts"],
)
@router.head("/id/{host_id}", include_in_schema=False)
async def get_host_by_id(host_id: conint(ge=0, lt=2**31)):
    """Retrieve a Host object, based on Host ID, containing: Host ID,
    name, slug string, and gender."""
    try:
        host = Host(database_connection=_database_connection)
        host_info = host.retrieve_by_id(host_id)
        if not host_info:
            raise HTTPException(status_code=404, detail=f"Host ID {host_id} not found")
        else:
            return host_info
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Host ID {host_id} not found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve host information",
        )


@router.get(
    "/slug/{host_slug}",
    summary="Retrieve Information by Host Slug String",
    response_model=ModelsHost,
    tags=["Hosts"],
)
@router.head("/slug/{host_slug}", include_in_schema=False)
async def get_host_by_slug(host_slug: constr(strip_whitespace=True)):
    """Retrieve a Host object, based on Host slug string, containing:
    Host ID, name, slug string, and gender."""
    try:
        host = Host(database_connection=_database_connection)
        host_info = host.retrieve_by_slug(host_slug)
        if not host_info:
            raise HTTPException(
                status_code=404, detail=f"Host slug string {host_slug} not found"
            )
        else:
            return host_info
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Host slug string {host_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve host information",
        )


@router.get(
    "/details",
    summary="Retrieve Information and Appearances for All Hosts",
    response_model=ModelsHostsDetails,
    tags=["Hosts"],
)
@router.head("/details", include_in_schema=False)
async def get_hosts_details():
    """Retrieve an array of Host objects, each containing: Host ID,
    name, slug string, gender, and their appearance details.

    Results are sorted by host name, with host apperances sorted by
    show date."""
    try:
        host = Host(database_connection=_database_connection)
        hosts = host.retrieve_all_details()
        if not hosts:
            raise HTTPException(status_code=404, detail="No hosts found")
        else:
            return {"hosts": hosts}
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve hosts from the database"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving "
            "hosts from the database",
        )


@router.get(
    "/details/id/{host_id}",
    summary="Retrieve Information and Appearances by Host ID",
    response_model=ModelsHostDetails,
    tags=["Hosts"],
)
@router.head("/details/id/{host_id}", include_in_schema=False)
async def get_host_details_by_id(host_id: conint(ge=0, lt=2**31)):
    """Retrieve a Host object, based on Host ID, containing: Host ID,
    name, slug string, gender, and their appearance details.

    Host appearances are sorted by show date."""
    try:
        host = Host(database_connection=_database_connection)
        host_details = host.retrieve_details_by_id(host_id)
        if not host_details:
            raise HTTPException(status_code=404, detail=f"Host ID {host_id} not found")
        else:
            return host_details
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Host ID {host_id} not found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve host information",
        )


@router.get(
    "/details/slug/{host_slug}",
    summary="Retrieve Information and Appearances by Host by Slug String",
    response_model=ModelsHostDetails,
    tags=["Hosts"],
)
@router.head("/details/slug/{host_slug}", include_in_schema=False)
async def get_host_details_by_slug(host_slug: constr(strip_whitespace=True)):
    """Retrieve a Host object, based on Host slug string, containing:
    Host ID, name, slug string, gender, and their appearance details.

    Host appearances are sorted by show date."""
    try:
        host = Host(database_connection=_database_connection)
        host_details = host.retrieve_details_by_slug(host_slug)
        if not host_details:
            raise HTTPException(
                status_code=404, detail=f"Host slug string {host_slug} not found"
            )
        else:
            return host_details
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Host slug string {host_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve host information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve host information",
        )


# endregion
