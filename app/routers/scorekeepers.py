# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Scorekeeper endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.scorekeeper import Scorekeeper

from app.config import API_VERSION, load_config
from app.models.messages import MessageDetails
from app.models.scorekeepers import Scorekeeper as ModelsScorekeeper
from app.models.scorekeepers import ScorekeeperDetails as ModelsScorekeeperDetails
from app.models.scorekeepers import ScorekeeperID as ModelsScorekeeperID
from app.models.scorekeepers import Scorekeepers as ModelsScorekeepers
from app.models.scorekeepers import ScorekeepersDetails as ModelsScorekeepersDetails
from app.models.scorekeepers import ScorekeeperSlug as ModelsScorekeeperSlug

router = APIRouter(prefix=f"/v{API_VERSION}/scorekeepers")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Scorekeepers",
    response_model=ModelsScorekeepers,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("", include_in_schema=False)
async def get_scorekeepers():
    """Retrieve All Scorekeepers.

    Returned data: Scorekeeper ID, name, slug string and gender.

    Scorekeepers are sorted by scorekeeper name.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeepers = scorekeeper.retrieve_all()
        if scorekeepers:
            return {"scorekeepers": scorekeepers}

        return JSONResponse(
            status_code=404, content={"detail": "No scorekeepers found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeepers from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving scorekeepers from the database"
            },
        )


@router.get(
    "/id/{scorekeeper_id}",
    summary="Retrieve Information by Scorekeeper ID",
    response_model=ModelsScorekeeper,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/id/{scorekeeper_id}", include_in_schema=False)
async def get_scorekeeper_by_id(
    scorekeeper_id: Annotated[
        int, Path(title="The ID of the scorekeeper to get", ge=0, lt=2**31)
    ],
):
    """Retrieve a Scorekeeper by Scorekeeper ID.

    Returned data: Scorekeeper ID, name, slug string and gender.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_info = scorekeeper.retrieve_by_id(scorekeeper_id)
        if scorekeeper_info:
            return scorekeeper_info

        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper ID {scorekeeper_id} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper ID {scorekeeper_id} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeeper information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve scorekeeper information"
            },
        )


@router.get(
    "/slug/{scorekeeper_slug}",
    summary="Retrieve Information by Scorekeeper Slug String",
    response_model=ModelsScorekeeper,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/slug/{scorekeeper_slug}", include_in_schema=False)
async def get_scorekeeper_by_slug(
    scorekeeper_slug: Annotated[
        str, Path(title="The slug string of the scorekeeper to get")
    ],
):
    """Retrieve a Scorekeeper by Scorekeeper Slug String.

    Returned data: Scorekeeper ID, name, slug string and gender.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_info = scorekeeper.retrieve_by_slug(scorekeeper_slug.strip())
        if scorekeeper_info:
            return scorekeeper_info

        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper slug string {scorekeeper_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper slug string {scorekeeper_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeeper information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve scorekeeper information"
            },
        )


@router.get(
    "/details",
    summary="Retrieve Information and Appearances for All Scorekeepers",
    response_model=ModelsScorekeepersDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/details", include_in_schema=False)
async def get_scorekeepers_details():
    """Retrieve Details for All Scorekeepers.

    Returned data: Scorekeepers ID, name, slug string, gender and
    appearances.

    Scorekeepers are sorted by scorekeeper name. Appearances are sorted
    by show date.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeepers = scorekeeper.retrieve_all_details()
        if scorekeepers:
            return {"scorekeepers": scorekeepers}

        return JSONResponse(
            status_code=404, content={"detail": "No scorekeepers found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeepers from the database"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving scorekeepers from the database"
            },
        )


@router.get(
    "/details/id/{scorekeeper_id}",
    summary="Retrieve Information and Appearances by Scorekeeper ID",
    response_model=ModelsScorekeeperDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/details/id/{scorekeeper_id}", include_in_schema=False)
async def get_scorekeeper_details_by_id(
    scorekeeper_id: Annotated[
        int, Path(title="The ID of the scorekeeper to get", ge=0, lt=2**31)
    ],
):
    """Retrieve Details for a Scorekeeper by Scorekeeper ID.

    Returned data: Scorekeeper ID, name, slug string, gender and
    appearances.

    Appearances are sorted by show date.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_details = scorekeeper.retrieve_details_by_id(scorekeeper_id)
        if scorekeeper_details:
            return scorekeeper_details

        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper ID {scorekeeper_id} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper ID {scorekeeper_id} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeeper information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve scorekeeper information"
            },
        )


@router.get(
    "/details/random",
    summary="Retrieve Information and Appearances for a Random Scorekeeper",
    response_model=ModelsScorekeeperDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/details/random", include_in_schema=False)
async def get_random_scorekeeper_details():
    """Retrieve a Random Scorekeeper.

    Returned data: Scorekeeper ID, name, slug string, gender, and
    appearances.

    Appearances are sorted by date.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_details = scorekeeper.retrieve_random_details()
        if scorekeeper_details:
            return scorekeeper_details

        return JSONResponse(
            status_code=404, content={"detail": "Random Scorekeeper not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Scorekeeper not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeeper information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve scorekeeper information"
            },
        )


@router.get(
    "/details/slug/{scorekeeper_slug}",
    summary="Retrieve Information and Appearances by Scorekeeper by Slug String",
    response_model=ModelsScorekeeperDetails,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/details/slug/{scorekeeper_slug}", include_in_schema=False)
async def get_scorekeeper_details_by_slug(
    scorekeeper_slug: Annotated[
        str, Path(title="The slug string of the scorekeeper to get")
    ],
):
    """Retrieve Details for a Scorekeeper by Scorekeeper ID.

    Returned data: Scorekeeper ID, name, slug string, gender and
    appearances.

    Appearances are sorted by show date.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_details = scorekeeper.retrieve_details_by_slug(
            scorekeeper_slug.strip()
        )
        if scorekeeper_details:
            return scorekeeper_details

        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper slug string {scorekeeper_slug} not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Scorekeeper slug string {scorekeeper_slug} not found"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeeper information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve scorekeeper information"
            },
        )


@router.get(
    "/random",
    summary="Retrieve Information for a Random Scorekeeper",
    response_model=ModelsScorekeeper,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/random", include_in_schema=False)
async def get_random_scorekeeper():
    """Retrieve a Random Scorekeeper.

    Returned data: Scorekeeper ID, name, slug string and gender.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_info = scorekeeper.retrieve_random()
        if scorekeeper_info:
            return scorekeeper_info

        return JSONResponse(
            status_code=404, content={"detail": "Random Scorekeeper not found"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Scorekeeper not found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve scorekeeper information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve scorekeeper information"
            },
        )


@router.get(
    "/random/id",
    summary="Retrieve a Random Scorekeeper ID",
    response_model=ModelsScorekeeperID,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/random/id", include_in_schema=False)
async def get_random_scorekeeper_id():
    """Retrieve a Random Scorekeeper ID.

    Returned data: Scorekeeper ID.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_id = scorekeeper.retrieve_random_id()
        if scorekeeper_id:
            return {"id": scorekeeper_id}

        return JSONResponse(
            status_code=404, content={"detail": "Random Scorekeeper ID not returned"}
        )
    except ValueError:
        return JSONResponse(
            status_code=404, content={"detail": "Random Scorekeeper ID not returned"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve a random scorekeeper ID"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a random scorekeeper ID"
            },
        )


@router.get(
    "/random/slug",
    summary="Retrieve a Random Scorekeeper Slug String",
    response_model=ModelsScorekeeperSlug,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["Scorekeepers"],
)
@router.head("/random/slug", include_in_schema=False)
async def get_random_scorekeeper_slug():
    """Retrieve a Random Scorekeeper Slug String.

    Returned data: Scorekeeper slug string.
    """
    try:
        scorekeeper = Scorekeeper(database_connection=_database_connection)
        scorekeeper_slug = scorekeeper.retrieve_random_slug()
        if scorekeeper_slug:
            return {"slug": scorekeeper_slug}

        return JSONResponse(
            status_code=404,
            content={"detail": "Random Scorekeeper slug string not returned"},
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={"detail": "Random Scorekeeper slug string not returned"},
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve a random scorekeeper slug string"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve a random scorekeeper slug string"
            },
        )
