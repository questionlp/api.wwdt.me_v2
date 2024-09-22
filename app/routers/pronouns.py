# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Pronouns endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, HTTPException, Path
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.pronoun import Pronouns

from app.config import API_VERSION, load_config
from app.models.pronouns import Pronouns as ModelsPronouns
from app.models.pronouns import PronounsInfoList as ModelsPronounsInfoList

router = APIRouter(prefix=f"/v{API_VERSION}/pronouns")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Pronouns",
    response_model=ModelsPronounsInfoList,
    tags=["Pronouns"],
)
@router.head("", include_in_schema=False)
async def get_pronouns():
    """Retrieve All Pronouns.

    Returned data: Pronouns ID and pronouns string

    Values are sorted by Pronouns ID.
    """
    try:
        _pronouns = Pronouns(database_connection=_database_connection)
        all_pronouns = _pronouns.retrieve_all()
        if all_pronouns:
            return {"pronouns": all_pronouns}

        raise HTTPException(status_code=404, detail="No pronouns found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve pronouns from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving pronouns from the database",
        ) from None


@router.get(
    "/id/{pronouns_id}",
    summary="Retrieve Information by Pronouns ID",
    response_model=ModelsPronouns,
    tags=["Pronouns"],
)
@router.head("/id/{pronouns_id}", include_in_schema=False)
async def get_pronouns_by_id(
    pronouns_id: Annotated[
        int, Path(title="The ID of the pronouns to get", ge=0, lt=2**31)
    ]
):
    """Retrieve a Pronouns String by Pronouns ID.

    Returned data: Pronouns ID and pronouns string
    """
    try:
        _pronouns = Pronouns(database_connection=_database_connection)
        pronouns_info = _pronouns.retrieve_by_id(pronouns_id)
        if pronouns_info:
            return pronouns_info

        raise HTTPException(
            status_code=404, detail=f"Pronouns ID {pronouns_id} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Pronouns ID {pronouns_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve pronouns information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve pronouns information",
        ) from None
