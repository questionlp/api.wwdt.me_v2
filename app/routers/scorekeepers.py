# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""API routes for Scorekeeper endpoints"""

from app.config import API_VERSION, load_database_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import conint, constr
from wwdtm.scorekeeper import Scorekeeper
from app.models.scorekeepers import (Scorekeeper as ModelsScorekeeper,
                                     Scorekeepers as ModelsScorekeepers,
                                     ScorekeeperDetails as ModelsScorekeeperDetails,
                                     ScorekeepersDetails as ModelsScorekeepersDetails)

router = APIRouter(
    prefix=f"/v{API_VERSION}/scorekeepers"
)
_database_config = load_database_config()
_database_connection = mysql.connector.connect(pool_name="wwdtm_api",
                                               **_database_config)


# region Routes
@router.get("",
            summary="Retrieve Information for All Scorekeepers",
            response_model=ModelsScorekeepers,
            tags=["Scorekeepers"])
@router.head("",
             include_in_schema=False)
async def get_scorekeepers():
    """Retrieve an array of Scorekeepers objects, each containing:
    Scorekeepers ID, name, slug string, and gender.

    Results are stored by scorekeeper name."""
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeepers = scorekeeper.retrieve_all()
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


@router.get("/id/{scorekeeper_id}",
            summary="Retrieve Information by Scorekeeper ID",
            response_model=ModelsScorekeeper,
            tags=["Scorekeepers"])
@router.head("/id/{scorekeeper_id}",
             include_in_schema=False)
async def get_scorekeeper_by_id(scorekeeper_id: conint(ge=0, lt=2**31)):
    """Retrieve a Scorekeeper object, based on Scorekeeper ID,
    containing: Scorekeeper ID, name, slug string, and gender."""
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_info = scorekeeper.retrieve_by_id(scorekeeper_id)
        if not scorekeeper_info:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper ID {scorekeeper_id} not found")
        else:
            return scorekeeper_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Scorekeeper ID {scorekeeper_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")


@router.get("/slug/{scorekeeper_slug}",
            summary="Retrieve Information by Scorekeeper Slug String",
            response_model=ModelsScorekeeper,
            tags=["Scorekeepers"])
@router.head("/slug/{scorekeeper_slug}",
             include_in_schema=False)
async def get_scorekeeper_by_slug(scorekeeper_slug: constr(strip_whitespace=True)):
    """Retrieve a Scorekeeper object, based on Scorekeeper slug string,
    containing: Scorekeeper ID, name, slug string, and gender."""
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_info = scorekeeper.retrieve_by_slug(scorekeeper_slug)
        if not scorekeeper_info:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper slug string {scorekeeper_slug} not found")
        else:
            return scorekeeper_info
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Scorekeeper slug string {scorekeeper_slug} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")


@router.get("/details",
            summary="Retrieve Information and Appearances for All Scorekeepers",
            response_model=ModelsScorekeepersDetails,
            tags=["Scorekeepers"])
@router.head("/details",
             include_in_schema=False)
async def get_scorekeepers_details():
    """Retrieve an array of Scorekeepers objects, each containing:
    Scorekeepers ID, name, slug string, gender, and their appearance
    details.

    Results are sorted by scorekeeper name, with scorekeeper apperances
    sorted by show date."""
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeepers = scorekeeper.retrieve_all_details()
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


@router.get("/details/id/{scorekeeper_id}",
            summary="Retrieve Information and Appearances by Scorekeeper ID",
            response_model=ModelsScorekeeperDetails,
            tags=["Scorekeepers"])
@router.head("/details/id/{scorekeeper_id}",
             include_in_schema=False)
async def get_scorekeeper_details_by_id(scorekeeper_id: conint(ge=0, lt=2**31)):
    """Retrieve a Scorekeeper object, based on Scorekeeper ID,
    containing: Scorekeeper ID, name, slug string, gender, and their
    appearance details.

    Scorekeeper appearances are sorted by show date."""
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_details = scorekeeper.retrieve_details_by_id(scorekeeper_id)
        if not scorekeeper_details:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper ID {scorekeeper_id} not found")
        else:
            return scorekeeper_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Scorekeeper ID {scorekeeper_id} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")


@router.get("/details/slug/{scorekeeper_slug}",
            summary="Retrieve Information and Appearances by Scorekeeper by Slug String",
            response_model=ModelsScorekeeperDetails,
            tags=["Scorekeepers"])
@router.head("/details/slug/{scorekeeper_slug}",
             include_in_schema=False)
async def get_scorekeeper_details_by_slug(scorekeeper_slug: constr(strip_whitespace=True)):
    """Retrieve a Scorekeeper object, based on Scorekeeper slug string,
    containing: Scorekeeper ID, name, slug string, gender, and their
    appearance details.

    Scorekeeper appearances are sorted by show date."""
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_details = scorekeeper.retrieve_details_by_slug(scorekeeper_slug)
        if not scorekeeper_details:
            raise HTTPException(status_code=404,
                                detail=f"Scorekeeper slug string {scorekeeper_slug} not found")
        else:
            return scorekeeper_details
    except ValueError:
        raise HTTPException(status_code=404,
                            detail=f"Scorekeeper slug string {scorekeeper_slug} not found")
    except ProgrammingError:
        raise HTTPException(status_code=500,
                            detail="Unable to retrieve scorekeeper information")
    except DatabaseError:
        raise HTTPException(status_code=500,
                            detail="Database error occurred while trying to "
                                   "retrieve scorekeeper information")

# endregion
