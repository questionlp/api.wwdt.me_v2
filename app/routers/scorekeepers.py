# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Scorekeeper endpoints"""

from app.config import API_VERSION, load_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import constr, PositiveInt
from wwdtm.scorekeeper import details, info
from app.models.scorekeepers import (Scorekeeper, Scorekeepers,
                                     ScorekeeperDetails,
                                     ScorekeepersDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/scorekeepers"
)
_app_config = load_config()
_database_connection = mysql.connector.connect(**_app_config)
_database_connection.autocommit = True

#region Routes
@router.get("/",
summary="Retrieve Information for All Scorekeepers",
            response_model=Scorekeepers,
            tags=["Scorekeepers"])
async def get_scorekeepers():
    """Retrieve an array of Scorekeepers objects, each containing:
    Scorekeepers ID, name, slug string, and gender.

    Results are stored by scorekeeper name."""
    try:
        _database_connection.reconnect()
        scorekeepers = info.retrieve_all(_database_connection)
        if not scorekeepers:
            raise HTTPException(status_code=404, detail="No scorekeepers found")
        else:
            return {"scorekeepers": scorekeepers}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeepers from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "scorekeepers from the database")


@router.get("/details",
            summary="Retrieve Information and Appearances for All Scorekeepers",
            response_model=ScorekeepersDetails,
            tags=["Scorekeepers"])
async def get_scorekeepers_details():
    """Retrieve an array of Scorekeepers objects, each containing:
    Scorekeepers ID, name, slug string, gender, and their appearance
    details.

    Results are sorted by scorekeeper name, with scorekeeper apperances
    sorted by show date."""
    try:
        _database_connection.reconnect()
        scorekeepers = details.retrieve_all(_database_connection)
        if not scorekeepers:
            raise HTTPException(status_code=404, detail="No scorekeepers found")
        else:
            return {"scorekeepers": scorekeepers}
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeepers from the database")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while retrieving "
                                   "scorekeepers from the database")


@router.get("/{scorekeeper_id}",
            summary="Retrieve Information by Scorekeeper ID",
            response_model=Scorekeeper,
            tags=["Scorekeepers"])
async def get_scorekeeper_by_id(scorekeeper_id: PositiveInt):
    """Retrieve a Scorekeeper object, based on Scorekeeper ID,
    containing: Scorekeeper ID, name, slug string, and gender."""
    try:
        _database_connection.reconnect()
        scorekeeper_info = info.retrieve_by_id(scorekeeper_id,
                                               _database_connection)
        if not scorekeeper_info:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper ID {scorekeeper_id} not found")
        else:
            return scorekeeper_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")


@router.get("/{scorekeeper_id}/details",
            summary="Retrieve Information and Appearances by Scorekeeper ID",
            response_model=ScorekeeperDetails,
            tags=["Scorekeepers"])
async def get_scorekeeper_details_by_id(scorekeeper_id: PositiveInt):
    """Retrieve a Scorekeeper object, based on Scorekeeper ID,
    containing: Scorekeeper ID, name, slug string, gender, and their
    appearance details.

    Scorekeeper appearances are sorted by show date."""
    try:
        _database_connection.reconnect()
        scorekeeper_details = details.retrieve_by_id(scorekeeper_id,
                                                     _database_connection)
        if not scorekeeper_details:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper ID {scorekeeper_id} not found")
        else:
            return scorekeeper_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")


@router.get("/slug/{scorekeeper_slug}",
            summary="Retrieve Information by Scorekeeper Slug String",
            response_model=Scorekeeper,
            tags=["Scorekeepers"])
async def get_scorekeeper_by_slug(scorekeeper_slug: constr(strip_whitespace = True)):
    """Retrieve a Scorekeeper object, based on Scorekeeper slug string,
    containing: Scorekeeper ID, name, slug string, and gender."""
    try:
        _database_connection.reconnect()
        scorekeeper_info = info.retrieve_by_slug(scorekeeper_slug,
                                                 _database_connection)
        if not scorekeeper_info:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper slug string {scorekeeper_slug} not found")
        else:
            return scorekeeper_info
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")


@router.get("/slug/{scorekeeper_slug}/details",
            summary="Retrieve Information and Appearances by Scorekeeper by Slug String",
            response_model=ScorekeeperDetails,
            tags=["Scorekeepers"])
async def get_scorekeeper_details_by_slug(scorekeeper_slug: constr(strip_whitespace = True)):
    """Retrieve a Scorekeeper object, based on Scorekeeper slug string,
    containing: Scorekeeper ID, name, slug string, gender, and their
    appearance details.

    Scorekeeper appearances are sorted by show date."""
    try:
        _database_connection.reconnect()
        scorekeeper_details = details.retrieve_by_slug(scorekeeper_slug,
                                                       _database_connection)
        if not scorekeeper_details:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper ID {scorekeeper_slug} not found")
        else:
            return scorekeeper_details
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")

#endregion
