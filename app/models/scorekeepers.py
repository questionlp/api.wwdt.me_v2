# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Scorekeepers Models."""

from typing import Annotated

from pydantic import BaseModel, Field


class Scorekeeper(BaseModel):
    """Scorekeeper Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Scorekeeper ID")
    name: str = Field(title="Scorekeeper Name")
    slug: str | None = Field(default=None, title="Scorekeeper Slug String")
    gender: str | None = Field(default=None, title="Scorekeeper Gender")
    pronouns: list[str] | None = Field(
        default=None, title="Scorekeeper Preferred Pronouns"
    )


class Scorekeepers(BaseModel):
    """List of Scorekeepers."""

    scorekeepers: list[Scorekeeper] = Field(title="List of Scorekeepers")


class ScorekeeperAppearanceCounts(BaseModel):
    """Count of Show Appearances."""

    regular_shows: int | None = Field(
        default=None, title="Count of Regular Show Appearances"
    )
    all_shows: int | None = Field(default=None, title="Count of All Show Appearances")


class ScorekeeperAppearance(BaseModel):
    """Appearance Information."""

    show_id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    guest: bool = Field(title="Guest Scorekeeper")
    description: str | None = Field(default=None, title="Scorekeeper Introduction")


class ScorekeeperAppearances(BaseModel):
    """Scorekeeper Appearance Information."""

    count: ScorekeeperAppearanceCounts | int = Field(title="Count of Show Appearances")
    shows: list[ScorekeeperAppearance] | None = Field(
        default=None, title="List of Show Appearances"
    )


class ScorekeeperDetails(Scorekeeper):
    """Scorekeeper Information with Appearances."""

    appearances: ScorekeeperAppearances | None = Field(
        default=None, title="List of Show Appearances"
    )


class ScorekeepersDetails(BaseModel):
    """List of Scorekeeper Details."""

    scorekeepers: list[ScorekeeperDetails] = Field(title="List of Scorekeeper Details")
    scorekeepers: list[ScorekeeperDetails] = Field(title="List of Scorekeeper Details")
