# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI hosts router module for api.wwdt.me"""

from app.dependencies import API_VERSION, load_config
from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import BaseModel
from wwdtm.host import details, info

#region Host Models
class Host(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    gender: Optional[str] = None

class Hosts(BaseModel):
    hosts: List[Host]

class HostAppearanceCounts(BaseModel):
    regular_shows: int
    all_shows: int

class HostAppearance(BaseModel):
    show_id: int
    date: str
    best_of: bool
    repeat_show: bool
    guest: bool

class HostAppearances(BaseModel):
    count: Union[HostAppearanceCounts, int]
    shows: Optional[List[HostAppearance]] = None

class HostDetails(Host):
    appearances: Optional[HostAppearances] = None

class HostsDetails(BaseModel):
    hosts: List[HostDetails]

#endregion

router = APIRouter(
    prefix=f"/v{API_VERSION}/hosts"
)
_app_config = load_config()
_database_connection = mysql.connector.connect(**_app_config)
_database_connection.autocommit = True

#region Routes
@router.get("/", summary="Get Information for All Hosts",
            response_model=Hosts, tags=["Hosts"])
async def get_hosts():
    """Retrieve a list containing information all Hosts"""
    try:
        _database_connection.reconnect()
        hosts = info.retrieve_all(_database_connection)
        if not hosts:
            raise HTTPException(status_code=404, detail="No hosts found")
        else:
            return {"hosts": hosts}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve hosts from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "hosts from the database")


@router.get("/details",
            summary="Get Information and Appearances for All Hosts",
            response_model=HostsDetails, tags=["Hosts"])
async def get_hosts_details():
    """Retrieve a list containing information and appearances for all
    Hosts"""
    try:
        _database_connection.reconnect()
        hosts = details.retrieve_all(_database_connection)
        if not hosts:
            raise HTTPException(status_code=404, detail="No hosts found")
        else:
            return {"hosts": hosts}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve hosts from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "hosts from the database")


@router.get("/{host_id}",
            summary="Get Information by Host ID",
            response_model=Host, tags=["Hosts"])
async def get_host_by_id(host_id: int):
    """Retrieve information for a given Host ID"""
    try:
        _database_connection.reconnect()
        host_info = info.retrieve_by_id(host_id, _database_connection)
        if not host_info:
            raise HTTPException(status_code=404,
                                detail=f"Host ID {host_id} not found")
        else:
            return host_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")


@router.get("/{host_id}/details",
            summary="Get Information and Appearances by Host ID",
            response_model=HostDetails, tags=["Hosts"])
async def get_host_details_by_id(host_id: int):
    """Retrieve information and appearances for a given Host ID"""
    try:
        _database_connection.reconnect()
        host_details = details.retrieve_by_id(host_id, _database_connection)
        if not host_details:
            raise HTTPException(status_code=404,
                                detail=f"Host ID {host_id} not found")
        else:
            return host_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")


@router.get("/slug/{host_slug}",
            summary="Get Information by Host Slug String",
            response_model=Host, tags=["Hosts"])
async def get_host_by_slug(host_slug: str):
    """Retrieve information for a given Host slug string"""
    try:
        _database_connection.reconnect()
        host_info = info.retrieve_by_slug(host_slug, _database_connection)
        if not host_info:
            raise HTTPException(status_code=404,
                                detail=f"Host slug string {host_slug} not found")
        else:
            return host_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")


@router.get("/slug/{host_slug}/details",
            summary="Get Information and Appearances by Host by Slug String",
            response_model=HostDetails, tags=["Hosts"])
async def get_host_details_by_slug(host_slug: str):
    """Retrieve information and appearances for a given Host slug
    string"""
    try:
        _database_connection.reconnect()
        host_details = details.retrieve_by_slug(host_slug, _database_connection)
        if not host_details:
            raise HTTPException(status_code=404,
                                detail=f"Host ID {host_slug} not found")
        else:
            return host_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve host information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve host information")

#endregion
