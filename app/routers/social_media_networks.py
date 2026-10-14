# Copyright (c) 2018-2026 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""API routes for Hosts endpoints."""

from typing import Annotated

import mysql.connector
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from mysql.connector.errors import DatabaseError, ProgrammingError
from wwdtm.social_media import SocialMediaNetworks

from app.config import API_VERSION, load_config
from app.models.messages import MessageDetails
from app.models.social_media import SocialMediaNetwork as ModelSocialMediaNetwork
from app.models.social_media import SocialMediaNetworks as ModelSocialMediaNetworks

router = APIRouter(prefix=f"/v{API_VERSION}/social-media-networks")
_config = load_config()
_database_config = _config["database"]
_database_connection = mysql.connector.connect(**_database_config)


@router.get(
    "",
    summary="Retrieve Information for All Available Social Media Networks",
    response_model=ModelSocialMediaNetworks,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["SocialMediaNetworks"],
)
@router.head("", include_in_schema=False)
async def get_social_media_networks():
    """Retrieve All Available Social Media Networks.

    Returned data: Social Media Network ID, network name and slug string.

    Values are stored by Social Media Network ID.
    """
    try:
        smn = SocialMediaNetworks(database_connection=_database_connection)
        networks = smn.retrieve_all()

        if networks:
            return {"networks": networks}

        return JSONResponse(
            status_code=404, content={"detail": "No social media networks found"}
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Unable to retrieve social media networks from the database"
            },
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while retrieving social media networks from the database"
            },
        )


@router.get(
    "/id/{social_media_network_id}",
    summary="Retrieve Information by Social Media Network ID",
    response_model=ModelSocialMediaNetwork,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["SocialMediaNetworks"],
)
@router.head("/id/{social_media_network_id}", include_in_schema=False)
async def get_social_media_network_by_id(
    social_media_network_id: Annotated[
        int, Path(title="The ID of the social media network to get", ge=0, lt=2**31)
    ],
):
    """Retrieve a Social Media Network by Social Media Network ID.

    Returned data: Social Media Network ID, network name and slug string.
    """
    try:
        smn = SocialMediaNetworks(database_connection=_database_connection)
        network_info = smn.retrieve_by_id(social_media_network_id)

        if network_info:
            return network_info

        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Social Media Network ID {social_media_network_id} not found"
            },
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Social Media Network ID {social_media_network_id} not found"
            },
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve social media network information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve social media network information"
            },
        )


@router.get(
    "/slug/{social_media_network_slug}",
    summary="Retrieve Information by Social Media Network Slug String",
    response_model=ModelSocialMediaNetwork,
    responses={404: {"model": MessageDetails}, 500: {"model": MessageDetails}},
    tags=["SocialMediaNetworks"],
)
@router.head("/slug/{social_media_network_slug}", include_in_schema=False)
async def get_social_media_network_by_slug(
    social_media_network_slug: Annotated[
        str, Path(title="The slug string of the social media network to get")
    ],
):
    """Retrieve a Social Media Network by Social Media Network Slug String.

    Returned data: Social Media Network ID, network name and slug string.
    """
    try:
        smn = SocialMediaNetworks(database_connection=_database_connection)
        network_info = smn.retrieve_by_slug(social_media_network_slug)

        if network_info:
            return network_info

        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Social Media Network slug string {social_media_network_slug} not found"
            },
        )
    except ValueError:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Social Media Network slug string {social_media_network_slug} not found"
            },
        )
    except ProgrammingError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unable to retrieve social media network information"},
        )
    except DatabaseError:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Database error occurred while trying to retrieve social media network information"
            },
        )
