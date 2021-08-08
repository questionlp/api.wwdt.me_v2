# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Hosts endpoints"""

from app.config import API_VERSION, load_database_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import constr, PositiveInt
from wwdtm.host import details, info
from app.models.hosts import (Host, Hosts, HostDetails, HostsDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/hosts"
)
_database_config = load_database_config()
_database_connection = mysql.connector.connect(**_database_config)
_database_connection.autocommit = True

#region Routes
@router.get("",
            summary="Retrieve Information for All Hosts",
            response_model=Hosts,
            tags=["Hosts"])
async def get_hosts():
    """Retrieve an array of Host objects, each containing: Host ID,
    name, slug string, and gender.

    Results are sorted by host name."""
    try:
        _database_connection.reconnect()
        hosts = info.retrieve_all(_database_connection)
        if not hosts:
            raise HTTPException(status_code=404,
                                detail="No hosts found")
        else:
            return {"hosts": hosts}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve hosts from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "hosts from the database")


@router.get("/id/{host_id}",
            summary="Retrieve Information by Host ID",
            response_model=Host,
            tags=["Hosts"])
async def get_host_by_id(host_id: PositiveInt):
    """Retrieve a Host object, based on Host ID, containing: Host ID,
    name, slug string, and gender."""
    try:
        _database_connection.reconnect()
        host_info = info.retrieve_by_id(host_id,
                                        _database_connection)
        if not host_info:
            raise HTTPException(status_code=404,
                                detail=f"Host ID {host_id} not found")
        else:
            return host_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Host ID {host_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")


@router.get("/slug/{host_slug}",
            summary="Retrieve Information by Host Slug String",
            response_model=Host,
            tags=["Hosts"])
async def get_host_by_slug(host_slug: constr(strip_whitespace = True)):
    """Retrieve a Host object, based on Host slug string, containing:
    Host ID, name, slug string, and gender."""
    try:
        _database_connection.reconnect()
        host_info = info.retrieve_by_slug(host_slug,
                                          _database_connection)
        if not host_info:
            raise HTTPException(status_code=404,
                                detail=f"Host slug string {host_slug} not found")
        else:
            return host_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Host slug string {host_slug} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")


@router.get("/details",
            summary="Retrieve Information and Appearances for All Hosts",
            response_model=HostsDetails,
            tags=["Hosts"])
async def get_hosts_details():
    """Retrieve an array of Host objects, each containing: Host ID,
    name, slug string, gender, and their appearance details.

    Results are sorted by host name, with host apperances sorted by
    show date."""
    try:
        _database_connection.reconnect()
        hosts = details.retrieve_all(_database_connection)
        if not hosts:
            raise HTTPException(status_code=404,
                                detail="No hosts found")
        else:
            return {"hosts": hosts}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve hosts from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "hosts from the database")


@router.get("/details/id/{host_id}",
            summary="Retrieve Information and Appearances by Host ID",
            response_model=HostDetails,
            tags=["Hosts"])
async def get_host_details_by_id(host_id: PositiveInt):
    """Retrieve a Host object, based on Host ID, containing: Host ID,
    name, slug string, gender, and their appearance details.

    Host appearances are sorted by show date."""
    try:
        _database_connection.reconnect()
        host_details = details.retrieve_by_id(host_id,
                                              _database_connection)
        if not host_details:
            raise HTTPException(status_code=404,
                                detail=f"Host ID {host_id} not found")
        else:
            return host_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Host ID {host_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")


@router.get("/details/slug/{host_slug}",
            summary="Retrieve Information and Appearances by Host by Slug String",
            response_model=HostDetails,
            tags=["Hosts"])
async def get_host_details_by_slug(host_slug: constr(strip_whitespace = True)):
    """Retrieve a Host object, based on Host slug string, containing:
    Host ID, name, slug string, gender, and their appearance details.

    Host appearances are sorted by show date."""
    try:
        _database_connection.reconnect()
        host_details = details.retrieve_by_slug(host_slug,
                                                _database_connection)
        if not host_details:
            raise HTTPException(status_code=404,
                                detail=f"Host slug string {host_slug} not found")
        else:
            return host_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Host slug string {host_slug} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")

#endregion
