# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Panelists endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, HTTPException, Path
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.panelist import Panelist, PanelistDecimalScores, PanelistScores

from app.config import API_VERSION, load_config
from app.models.panelists import Panelist as ModelsPanelist
from app.models.panelists import PanelistDetails as ModelsPanelistDetails
from app.models.panelists import Panelists as ModelsPanelists
from app.models.panelists import (
    PanelistScoresGroupedOrderedPair as ModelsPanelistScoresGroupedOrderedPair,
)
from app.models.panelists import PanelistScoresList as ModelsPanelistScoresList
from app.models.panelists import (
    PanelistScoresOrderedPair as ModelsPanelistScoresOrderedPair,
)
from app.models.panelists import PanelistsDetails as ModelsPanelistsDetails

router = APIRouter(prefix=f"/v{API_VERSION}/panelists")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Panelists",
    response_model=ModelsPanelists,
    tags=["Panelists"],
)
@router.head("", include_in_schema=False)
async def get_panelists():
    """Retrieve All Panelists.

    Returned data: Panelist ID, name, slug string and gender.

    Panelists are sorted by panelist name.
    """
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelists = panelist.retrieve_all()
        if panelists:
            return {"panelists": panelists}

        raise HTTPException(status_code=404, detail="No panelists found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelists from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving panelists from the database",
        ) from None


@router.get(
    "/id/{panelist_id}",
    summary="Retrieve Information by Panelist ID",
    response_model=ModelsPanelist,
    tags=["Panelists"],
)
@router.head("/id/{panelist_id}", include_in_schema=False)
async def get_panelist_by_id(
    panelist_id: Annotated[
        int, Path(title="The ID of the panelist to get", ge=0, lt=2**31)
    ],
):
    """Retrieve a Panelist by Panelist ID.

    Returned data: Panelist ID, name, slug string and gender.
    """
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_info = panelist.retrieve_by_id(panelist_id)
        if panelist_info:
            return panelist_info

        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist information",
        ) from None


@router.get(
    "/slug/{panelist_slug}",
    summary="Retrieve Information by Panelist Slug String",
    response_model=ModelsPanelist,
    tags=["Panelists"],
)
@router.head("/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_by_slug(
    panelist_slug: Annotated[str, Path(title="The slug string of the panelist to get")],
):
    """Retrieve a Panelist by Panelist Slug String.

    Returned data: Panelist ID, name, slug string and gender.
    """
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_info = panelist.retrieve_by_slug(panelist_slug.strip())
        if panelist_info:
            return panelist_info

        raise HTTPException(
            status_code=404,
            detail=f"Panelist slug string {panelist_slug} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist information",
        ) from None


@router.get(
    "/details",
    summary="Retrieve Information, Statistics, and Appearances for All Panelists",
    response_model=ModelsPanelistsDetails,
    tags=["Panelists"],
)
@router.head("/details", include_in_schema=False)
async def get_panelists_details():
    """Retrieve Details for All Panelists.

    Returned data: Panelists ID, name, slug string, gender, statistics
    and appearances.

    Panelists are sorted by panelist name. Appearances are sorted by
    date.
    """
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelists = panelist.retrieve_all_details(
            use_decimal_scores=_config["settings"]["use_decimal_scores"]
        )
        if panelists:
            return {"panelists": panelists}

        raise HTTPException(status_code=404, detail="No panelists found")
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelists from the database"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving panelists from the database",
        ) from None


@router.get(
    "/details/id/{panelist_id}",
    summary="Retrieve Information, Statistics, and Appearances by Panelist ID",
    response_model=ModelsPanelistDetails,
    tags=["Panelists"],
)
@router.head("/details/id/{panelist_id}", include_in_schema=False)
async def get_panelist_details_by_id(
    panelist_id: Annotated[
        int, Path(title="The ID of the panelist to get", ge=0, lt=2**31)
    ],
):
    """Retrieve Details for a Panelist by Panelist ID.

    Returned data: Panelist ID, name, slug string, gender, statistics
    and appearances.

    Appearances are sorted by date.
    """
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_details = panelist.retrieve_details_by_id(
            panelist_id, use_decimal_scores=_config["settings"]["use_decimal_scores"]
        )
        if panelist_details:
            return panelist_details

        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist information",
        ) from None


@router.get(
    "/details/slug/{panelist_slug}",
    summary="Retrieve Information, Statistics and Appearances by Panelist by Slug String",
    response_model=ModelsPanelistDetails,
    tags=["Panelists"],
)
@router.head("/details/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_details_by_slug(
    panelist_slug: Annotated[str, Path(title="The slug string of the panelist to get")],
):
    """Retrieve Details for a Panelist by Panelist Slug String.

    Returned data: Panelist ID, name, slug string, gender, statistics
    and appearances.

    Appearances are sorted by date.
    """
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_details = panelist.retrieve_details_by_slug(
            panelist_slug.strip(),
            use_decimal_scores=_config["settings"]["use_decimal_scores"],
        )
        if panelist_details:
            return panelist_details

        raise HTTPException(
            status_code=404,
            detail=f"Panelist slug string {panelist_slug} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist information",
        ) from None


@router.get(
    "/scores/id/{panelist_id}",
    summary="Retrieve Panelist Scores for Each Appearance by Panelist ID",
    response_model=ModelsPanelistScoresList,
    tags=["Panelists"],
)
@router.head("/scores/id/{panelist_id}", include_in_schema=False)
async def get_panelist_scores_by_id(
    panelist_id: Annotated[
        int, Path(title="The ID of the panelist to get", ge=0, lt=2**31)
    ],
):
    """Retrieve Panelist Scores by Panelist ID.

    Returned data: One array with show dates and one array with scores.
    """
    try:
        if _config["settings"]["use_decimal_scores"]:
            panelist_scores = PanelistDecimalScores(
                database_connection=_database_connection
            )
            scores = panelist_scores.retrieve_scores_list_by_id(
                panelist_id,
            )
        else:
            panelist_scores = PanelistScores(database_connection=_database_connection)
            scores = panelist_scores.retrieve_scores_list_by_id(panelist_id)
        if scores:
            return scores

        raise HTTPException(
            status_code=404,
            detail=f"Scoring data for Panelist ID {panelist_id} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist scores",
        ) from None


@router.get(
    "/scores/slug/{panelist_slug}",
    summary="Retrieve Panelist Scores for Each Appearance by Panelist Slug String",
    response_model=ModelsPanelistScoresList,
    tags=["Panelists"],
)
@router.head("/scores/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_scores_by_slug(
    panelist_slug: Annotated[str, Path(title="The slug string of the panelist to get")],
):
    """Retrieve Panelist Scores by Panelist Slug String.

    Returned data: One array with show dates and one array with scores.
    """
    try:
        if _config["settings"]["use_decimal_scores"]:
            panelist_scores = PanelistDecimalScores(
                database_connection=_database_connection
            )
            scores = panelist_scores.retrieve_scores_list_by_slug(panelist_slug.strip())
        else:
            panelist_scores = PanelistScores(database_connection=_database_connection)
            scores = panelist_scores.retrieve_scores_list_by_slug(panelist_slug.strip())
        if scores:
            return scores

        raise HTTPException(
            status_code=404,
            detail=f"Scoring data for Panelist slug string {panelist_slug} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist scores",
        ) from None


@router.get(
    "/scores/grouped-ordered-pair/id/{panelist_id}",
    summary=(
        "Retrieve Panelist Scores as Ordered Pairs for Scores and Number of "
        "Times It Has Been Earned by Panelist ID"
    ),
    response_model=ModelsPanelistScoresGroupedOrderedPair,
    tags=["Panelists"],
)
@router.head("/scores/grouped-ordered-pair/id/{panelist_id}", include_in_schema=False)
async def get_panelist_scores_grouped_ordered_pair_by_id(
    panelist_id: Annotated[
        int, Path(title="The ID of the panelist to get", ge=0, lt=2**31)
    ],
):
    """Retrieve Panelist Grouped Scores by Panelist ID.

    Returned data: Array of two element arrays: one element with a score
    and one element with corresponding score count.
    """
    try:
        if _config["settings"]["use_decimal_scores"]:
            panelist_scores = PanelistDecimalScores(
                database_connection=_database_connection
            )
            scores = panelist_scores.retrieve_scores_grouped_ordered_pair_by_id(
                panelist_id
            )
        else:
            panelist_scores = PanelistScores(database_connection=_database_connection)
            scores = panelist_scores.retrieve_scores_grouped_ordered_pair_by_id(
                panelist_id
            )
        if scores:
            return {"scores": scores}

        raise HTTPException(
            status_code=404,
            detail=f"Scoring data for Panelist ID {panelist_id} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist scores",
        ) from None


@router.get(
    "/scores/grouped-ordered-pair/slug/{panelist_slug}",
    summary=(
        "Retrieve Panelist Scores as Ordered Pairs for Scores and Number of "
        "Times It Has Been Earned by Panelist Slug String"
    ),
    response_model=ModelsPanelistScoresGroupedOrderedPair,
    tags=["Panelists"],
)
@router.head(
    "/scores/grouped-ordered-pair/slug/{panelist_slug}", include_in_schema=False
)
async def get_panelist_scores_grouped_ordered_pair_by_slug(
    panelist_slug: Annotated[str, Path(title="The slug string of the panelist to get")],
):
    """Retrieve Panelist Grouped Scores by Panelist Slug String.

    Returned data: Array of two element arrays: one element with a score
    and one element with corresponding score count.
    """
    try:
        if _config["settings"]["use_decimal_scores"]:
            panelist_scores = PanelistDecimalScores(
                database_connection=_database_connection
            )
            scores = panelist_scores.retrieve_scores_grouped_ordered_pair_by_slug(
                panelist_slug.strip()
            )
        else:
            panelist_scores = PanelistScores(database_connection=_database_connection)
            scores = panelist_scores.retrieve_scores_grouped_ordered_pair_by_slug(
                panelist_slug.strip()
            )
        if scores:
            return {"scores": scores}

        raise HTTPException(
            status_code=404,
            detail=f"Scoring data for Panelist slug string {panelist_slug} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist scores",
        ) from None


@router.get(
    "/scores/ordered-pair/id/{panelist_id}",
    summary="Retrieve Panelist Scores as Ordered Pairs by Panelist ID",
    response_model=ModelsPanelistScoresOrderedPair,
    tags=["Panelists"],
)
@router.head("/scores/ordered-pair/id/{panelist_id}", include_in_schema=False)
async def get_panelist_scores_ordered_pair_by_id(
    panelist_id: Annotated[
        int, Path(title="The ID of the panelist to get", ge=0, lt=2**31)
    ],
):
    """Retrieve Panelist Scores as Ordered Pairs by Panelist ID.

    Returned data: Array of two element arrays: one element with a show
    date and one element with corresponding score.
    """
    try:
        if _config["settings"]["use_decimal_scores"]:
            panelist_scores = PanelistDecimalScores(
                database_connection=_database_connection
            )
            scores = panelist_scores.retrieve_scores_ordered_pair_by_id(panelist_id)
        else:
            panelist_scores = PanelistScores(database_connection=_database_connection)
            scores = panelist_scores.retrieve_scores_ordered_pair_by_id(panelist_id)
        if scores:
            return {"scores": scores}

        raise HTTPException(
            status_code=404,
            detail=f"Scoring data for Panelist ID {panelist_id} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist scores",
        ) from None


@router.get(
    "/scores/ordered-pair/slug/{panelist_slug}",
    summary="Retrieve Panelist Scores as Ordered Pairs by Panelist Slug String",
    response_model=ModelsPanelistScoresOrderedPair,
    tags=["Panelists"],
)
@router.head("/scores/ordered-pair/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_scores_ordered_pair_by_slug(
    panelist_slug: Annotated[str, Path(title="The slug string of the panelist to get")],
):
    """Retrieve Panelist Scores as Ordered Pairs by Panelist Slug String.

    Returned data: Array of two element arrays: one element with a show
    date and one element with corresponding score.
    """
    try:
        if _config["settings"]["use_decimal_scores"]:
            panelist_scores = PanelistDecimalScores(
                database_connection=_database_connection
            )
            scores = panelist_scores.retrieve_scores_ordered_pair_by_slug(
                panelist_slug.strip()
            )
        else:
            panelist_scores = PanelistScores(database_connection=_database_connection)
            scores = panelist_scores.retrieve_scores_ordered_pair_by_slug(
                panelist_slug.strip()
            )
        if scores:
            return {"scores": scores}

        raise HTTPException(
            status_code=404,
            detail=f"Scoring data for Panelist slug string {panelist_slug} not found",
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        ) from None
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        ) from None
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to retrieve panelist scores",
        ) from None
