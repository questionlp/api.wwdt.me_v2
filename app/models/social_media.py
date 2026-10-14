# Copyright (c) 2018-2026 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Social Media Networks Models."""

from typing import Annotated

from pydantic import BaseModel, Field


class SocialMediaNetwork(BaseModel):
    """Social Media Network Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Social Media Network ID")
    network: str = Field(title="Social Media Network Name")
    slug: str | None = Field(default=None, title="Social Media Network Slug String")


class SocialMediaNetworks(BaseModel):
    """List of Social Media Networks."""

    networks: list[SocialMediaNetwork] = Field(title="List of Social Media Networks")


class SocialMediaNetworkAccount(BaseModel):
    """Social Media Network Account Information."""

    network: str = Field(title="Social Media Network")
    network_slug: str | None = Field(
        default=None, title="Social Media Network Slug String"
    )
    account: str = Field(title="Social Media Network Account")
    url: str = Field(title="Social Media Network Account URL")
