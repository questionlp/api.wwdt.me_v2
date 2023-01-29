# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""API routes for Panelists endpoints"""

from app.config import API_VERSION, load_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import conint, constr
from wwdtm.panelist import Panelist, PanelistScores
from app.models.panelists import (
    Panelist as ModelsPanelist,
    Panelists as ModelsPanelists,
    PanelistDetails as ModelsPanelistDetails,
    PanelistsDetails as ModelsPanelistsDetails,
    PanelistScoresList as ModelsPanelistScoresList,
    PanelistScoresOrderedPair as ModelsPanelistScoresOrderedPair,
    PanelistScoresGroupedOrderedPair as ModelsPanelistScoresGroupedOrderedPair,
)

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
    """Retrieve an array of Panelist objects, each containing: Panelist
    ID, name, slug string, and gender.

    Results are sorted by panelist name."""
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelists = panelist.retrieve_all()
        if not panelists:
            raise HTTPException(status_code=404, detail="No panelists found")
        else:
            return {"panelists": panelists}
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelists from the database"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving "
            "panelists from the database",
        )


@router.get(
    "/id/{panelist_id}",
    summary="Retrieve Information by Panelist ID",
    response_model=ModelsPanelist,
    tags=["Panelists"],
)
@router.head("/id/{panelist_id}", include_in_schema=False)
async def get_panelist_by_id(panelist_id: conint(ge=0, lt=2**31)):
    """Retrieve a Panelist object, based on Panelist ID, containing:
    Panelist ID, name, slug string, and gender."""
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_info = panelist.retrieve_by_id(panelist_id)
        if not panelist_info:
            raise HTTPException(
                status_code=404, detail=f"Panelist ID {panelist_id} not found"
            )
        else:
            return panelist_info
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist information",
        )


@router.get(
    "/slug/{panelist_slug}",
    summary="Retrieve Information by Panelist Slug String",
    response_model=ModelsPanelist,
    tags=["Panelists"],
)
@router.head("/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_by_slug(panelist_slug: constr(strip_whitespace=True)):
    """Retrieve a Panelist object, based on Panelist slug string,
    containing: Panelist ID, name, slug string, and gender."""
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_info = panelist.retrieve_by_slug(panelist_slug)
        if not panelist_info:
            raise HTTPException(
                status_code=404,
                detail=f"Panelist slug string {panelist_slug} not found",
            )
        else:
            return panelist_info
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist information",
        )


@router.get(
    "/details",
    summary="Retrieve Information, Statistics, and Appearances for All Panelists",
    response_model=ModelsPanelistsDetails,
    tags=["Panelists"],
)
@router.head("/details", include_in_schema=False)
async def get_panelists_details():
    """Retrieve an array of Panelists objects, each containing:
    Panelists ID, name, slug string, gender, and their statistics
    and appearance details.

    Results are sorted by panelist name, with panelist apperances
    sorted by show date."""
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelists = panelist.retrieve_all_details()
        if not panelists:
            raise HTTPException(status_code=404, detail="No panelists found")
        else:
            return {"panelists": panelists}
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelists from the database"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving "
            "panelists from the database",
        )


@router.get(
    "/details/id/{panelist_id}",
    summary="Retrieve Information, Statistics, and Appearances by Panelist ID",
    response_model=ModelsPanelistDetails,
    tags=["Panelists"],
)
@router.head("/details/id/{panelist_id}", include_in_schema=False)
async def get_panelist_details_by_id(panelist_id: conint(ge=0, lt=2**31)):
    """Retrieve a Panelist object, based on Panelist ID, containing:
    Panelist ID, name, slug string, gender, and their statistics and
    appearance details.

    Panelist appearances are sorted by show date."""
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_details = panelist.retrieve_details_by_id(panelist_id)
        if not panelist_details:
            raise HTTPException(
                status_code=404, detail=f"Panelist ID {panelist_id} not found"
            )
        else:
            return panelist_details
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist information",
        )


@router.get(
    "/details/slug/{panelist_slug}",
    summary="Retrieve Information, Statistics and Appearances by Panelist by Slug String",
    response_model=ModelsPanelistDetails,
    tags=["Panelists"],
)
@router.head("/details/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_details_by_slug(panelist_slug: constr(strip_whitespace=True)):
    """Retrieve a Panelist object, based on Panelist slug string,
    containing: Panelist ID, name, slug string, gender, and their
    statistics and appearance details.

    Panelist appearances are sorted by show date."""
    try:
        panelist = Panelist(database_connection=_database_connection)
        panelist_details = panelist.retrieve_details_by_slug(panelist_slug)
        if not panelist_details:
            raise HTTPException(
                status_code=404,
                detail=f"Panelist slug string {panelist_slug} not found",
            )
        else:
            return panelist_details
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist information"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist information",
        )


@router.get(
    "/scores/id/{panelist_id}",
    summary="Retrieve Panelist Scores for Each Appearance by Panelist ID",
    response_model=ModelsPanelistScoresList,
    tags=["Panelists"],
)
@router.head("/scores/id/{panelist_id}", include_in_schema=False)
async def get_panelist_scores_by_id(panelist_id: conint(ge=0, lt=2**31)):
    """Retrieve Panelist scores, based on Panelist ID, as a pair of
    lists, one list of show dates and one list of corresponding scores."""
    try:
        panelist_scores = PanelistScores(database_connection=_database_connection)
        scores = panelist_scores.retrieve_scores_list_by_id(panelist_id)
        if not scores:
            raise HTTPException(
                status_code=404,
                detail=f"Scoring data for Panelist ID {panelist_id} not found",
            )
        else:
            return scores
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist scores",
        )


@router.get(
    "/scores/slug/{panelist_slug}",
    summary="Retrieve Panelist Scores for Each Appearance by Panelist Slug String",
    response_model=ModelsPanelistScoresList,
    tags=["Panelists"],
)
@router.head("/scores/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_scores_by_slug(panelist_slug: constr(strip_whitespace=True)):
    """Retrieve Panelist scores, based on Panelist slug string, as a
    pair of lists, one list of show dates and one list of corresponding
    scores."""
    try:
        panelist_scores = PanelistScores(database_connection=_database_connection)
        scores = panelist_scores.retrieve_scores_list_by_slug(panelist_slug)
        if not scores:
            raise HTTPException(
                status_code=404,
                detail=f"Scoring data for Panelist slug string {panelist_slug} not found",
            )
        else:
            return scores
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist scores",
        )


@router.get(
    "/scores/grouped-ordered-pair/id/{panelist_id}",
    summary="Retrieve Panelist Scores as Ordered Pairs for Scores and Number "
    "of Times It Has Been Earned by Panelist ID",
    response_model=ModelsPanelistScoresGroupedOrderedPair,
    tags=["Panelists"],
)
@router.head("/scores/grouped-ordered-pair/id/{panelist_id}", include_in_schema=False)
async def get_panelist_scores_grouped_ordered_pair_by_id(
    panelist_id: conint(ge=0, lt=2**31)
):
    """Retrieve Panelist scores, based on Panelist ID, as grouped
    ordered pairs, each pair containing a score and the corresponding
    number of times a panelist has earned that score.

    **Note**: OpenAPI 3.0 does not support representation of tuples in
    models. The output is in the form of `(int, int)`."""
    try:
        panelist_scores = PanelistScores(database_connection=_database_connection)
        scores = panelist_scores.retrieve_scores_grouped_ordered_pair_by_id(panelist_id)
        if not scores:
            raise HTTPException(
                status_code=404,
                detail=f"Scoring data for Panelist ID {panelist_id} not found",
            )
        else:
            return {"scores": scores}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist scores",
        )


@router.get(
    "/scores/grouped-ordered-pair/slug/{panelist_slug}",
    summary="Retrieve Panelist Scores as Ordered Pairs for Scores and Number "
    "of Times It Has Been Earned by Panelist Slug String",
    response_model=ModelsPanelistScoresGroupedOrderedPair,
    tags=["Panelists"],
)
@router.head(
    "/scores/grouped-ordered-pair/slug/{panelist_slug}", include_in_schema=False
)
async def get_panelist_scores_grouped_ordered_pair_by_slug(
    panelist_slug: constr(strip_whitespace=True),
):
    """Retrieve Panelist scores, based on Panelist slug string, as
    grouped ordered pairs, each pair containing a score and the
    corresponding number of times a panelist has earned that score.

    **Note**: OpenAPI 3.0 does not support representation of tuples in
    models. The output is in the form of `(int, int)`."""
    try:
        panelist_scores = PanelistScores(database_connection=_database_connection)
        scores = panelist_scores.retrieve_scores_grouped_ordered_pair_by_slug(
            panelist_slug
        )
        if not scores:
            raise HTTPException(
                status_code=404,
                detail=f"Scoring data for Panelist slug string {panelist_slug} not found",
            )
        else:
            return {"scores": scores}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist scores",
        )


@router.get(
    "/scores/ordered-pair/id/{panelist_id}",
    summary="Retrieve Panelist Scores as Ordered Pairs by Panelist ID",
    response_model=ModelsPanelistScoresOrderedPair,
    tags=["Panelists"],
)
@router.head("/scores/ordered-pair/id/{panelist_id}", include_in_schema=False)
async def get_panelist_scores_ordered_pair_by_id(panelist_id: conint(ge=0, lt=2**31)):
    """Retrieve Panelist scores, based on Panelist ID, as ordered
    pairs, each pair containing the show date and the corresponding
    score.

    **Note**: OpenAPI 3.0 does not support representation of tuples in
    models. The output is in the form of `(str, int)`."""
    try:
        panelist_scores = PanelistScores(database_connection=_database_connection)
        scores = panelist_scores.retrieve_scores_ordered_pair_by_id(panelist_id)
        if not scores:
            raise HTTPException(
                status_code=404,
                detail=f"Scoring data for Panelist ID {panelist_id} not found",
            )
        else:
            return {"scores": scores}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist ID {panelist_id} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist scores",
        )


@router.get(
    "/scores/ordered-pair/slug/{panelist_slug}",
    summary="Retrieve Panelist Scores as Ordered Pairs by Panelist Slug String",
    response_model=ModelsPanelistScoresOrderedPair,
    tags=["Panelists"],
)
@router.head("/scores/ordered-pair/slug/{panelist_slug}", include_in_schema=False)
async def get_panelist_scores_ordered_pair_by_slug(
    panelist_slug: constr(strip_whitespace=True),
):
    """Retrieve Panelist scores, based on Panelist slug string, as
    ordered pairs, each pair containing the show date and the
    corresponding score.

    **Note**: OpenAPI 3.0 does not support representation of tuples in
    models. The output is in the form of `(str, int)`."""
    try:
        panelist_scores = PanelistScores(database_connection=_database_connection)
        scores = panelist_scores.retrieve_scores_ordered_pair_by_slug(panelist_slug)
        if not scores:
            raise HTTPException(
                status_code=404,
                detail=f"Scoring data for Panelist slug string {panelist_slug} not found",
            )
        else:
            return {"scores": scores}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Panelist slug string {panelist_slug} not found"
        )
    except ProgrammingError:
        raise HTTPException(
            status_code=500, detail="Unable to retrieve panelist scores"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while trying to "
            "retrieve panelist scores",
        )
