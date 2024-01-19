# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Hosts Models."""

from typing import Annotated

from pydantic import BaseModel, Field


class Host(BaseModel):
    """Host Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Host ID")
    name: str = Field(title="Host Name")
    slug: str | None = Field(default=None, title="Host Slug String")
    gender: str | None = Field(default=None, title="Host Gender")


class Hosts(BaseModel):
    """List of Hosts."""

    hosts: list[Host] = Field(title="List of Hosts")


class HostAppearanceCounts(BaseModel):
    """Count of Show Appearances."""

    regular_shows: int | None = Field(
        default=None, title="Count of Regular Show Appearances"
    )
    all_shows: int | None = Field(default=None, title="Count of All Show Appearances")


class HostAppearance(BaseModel):
    """Appearance Information."""

    show_id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    guest: bool = Field(title="Guest Host")


class HostAppearances(BaseModel):
    """Host Appearance Information."""

    count: HostAppearanceCounts | int = Field(title="Count of Show Appearances")
    shows: list[HostAppearance] | None = Field(
        default=None, title="List of Show Appearances"
    )


class HostDetails(Host):
    """Host Information with Appearances."""

    appearances: HostAppearances | None = Field(
        default=None, title="List of Show Appearances"
    )


class HostsDetails(BaseModel):
    """List of Host Details."""

    hosts: list[HostDetails] = Field(title="List of Host Details")
    hosts: list[HostDetails] = Field(title="List of Host Details")
