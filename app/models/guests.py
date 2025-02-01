# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Guests Models."""

from typing import Annotated

from pydantic import BaseModel, Field


class Guest(BaseModel):
    """Not My Job Guest Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Guest ID")
    name: str = Field(title="Guest Name")
    slug: str | None = Field(default=None, title="Guest Slug String")


class Guests(BaseModel):
    """List of Not My Job Guests."""

    guests: list[Guest] = Field(title="List of Guests")


class GuestAppearanceCounts(BaseModel):
    """Count of Show Appearances."""

    regular_shows: int | None = Field(
        default=None, title="Count of Regular Show Appearances"
    )
    all_shows: int | None = Field(default=None, title="Count of All Show Appearances")


class GuestAppearance(BaseModel):
    """Appearance Information."""

    show_id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    score: int | None = Field(default=None, title="Guest Score")
    score_exception: bool | None = Field(default=None, title="Guest Scoring Exception")


class GuestAppearances(BaseModel):
    """Not My Job Guest Appearances Information."""

    count: GuestAppearanceCounts | int = Field(title="Count of Show Appearances")
    shows: list[GuestAppearance] | None = Field(
        default=None, title="List of Show Appearances"
    )


class GuestDetails(Guest):
    """Not My Job Guest Information with Appearances."""

    appearances: GuestAppearances | None = Field(
        default=None, title="List of Show Appearances"
    )


class GuestsDetails(BaseModel):
    """List of Not My Job Guest Details."""

    guests: list[GuestDetails] = Field(title="List of Guest Details")
    guests: list[GuestDetails] = Field(title="List of Guest Details")


class GuestID(BaseModel):
    """Not My Job Guest ID."""

    id: int = Field(title="Guest ID")


class GuestSlug(BaseModel):
    """Not My Job Guest Slug String."""

    slug: str = Field(title="Guest Slug String")
