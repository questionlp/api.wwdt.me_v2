# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Shows Models."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field


class Show(BaseModel):
    """Show Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Best Of Show")
    show_url: str | None = Field(default=None, title="URL for Show Page on NPR.org")
    original_show_id: Annotated[int, Field(ge=0, lt=2**31)] | None = \
        Field(default=None, title="Original Show ID")
    original_show_date: str | None = Field(default=None, title="Original Show Date")


class Shows(BaseModel):
    """List of Shows."""

    shows: list[Show] = Field(title="List of Shows")


class ShowLocationCoordinates(BaseModel):
    """Coordinates for a Show Location."""

    latitude: Decimal | None = Field(default=None, title="Venue Latitude")
    longitude: Decimal | None = Field(default=None, title="Venue Longitude")


class ShowLocation(BaseModel):
    """Show Location Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Location ID")
    slug: str | None = Field(default=None, title="Location Slug String")
    city: str | None = Field(default=None, title="City")
    state: str | None = Field(default=None, title="State")
    venue: str | None = Field(default=None, title="Venue Name")
    coordinates: ShowLocationCoordinates | None = Field(
        default=None, title="Location Coordinates"
    )


class ShowHost(BaseModel):
    """Show Host Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Host ID")
    name: str = Field(title="Host Name")
    slug: str | None = Field(default=None, title="Host Slug String")
    guest: bool = Field(title="Guest Host")


class ShowScorekeeper(BaseModel):
    """Show Scorekeeper Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Scorekeeper ID")
    name: str = Field(title="Scorekeeper Name")
    slug: str | None = Field(default=None, title="Scorekeeper Slug String")
    guest: bool = Field(title="Guest Scorekeeper")
    description: str | None = Field(default=None, title="Scorekeeper Description")


class ShowPanelist(BaseModel):
    """Show Panelist Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: str | None = Field(default=None, title="Panelist Slug String")
    lightning_round_start: int | None = Field(
        default=None, title="Lightning Fill-in-the-Blank Starting Score"
    )
    lightning_round_start_decimal: Decimal | None = Field(
        default=None, title="Lightning Fill-in-the-Blank Starting Decimal Score"
    )
    lightning_round_correct: int | None = Field(
        default=None, title="Lightning Fill-in-the-Blank Correct Answers"
    )
    lightning_round_correct_decimal: Decimal | None = Field(
        default=None, title="Lightning Fill-in-the-Blank Correct Answers (Decimal)"
    )
    score: int | None = Field(default=None, title="Panelist Score")
    score_decimal: Decimal | None = Field(default=None, title="Panelist Decimal Score")
    rank: str | None = Field(default=None, title="Panelist Rank")


class ShowBluffPanelist(BaseModel):
    """Show Bluff the Listener Panelist Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: str | None = Field(default=None, title="Panelist Slug String")


class ShowBluffDetails(BaseModel):
    """Show Bluff the Listener Chosen and Correct Panelists."""

    segment: int = Field(title="Bluff Segment Number")
    chosen_panelist: ShowBluffPanelist | None = Field(
        default=None, title="Chosen Panelist"
    )
    correct_panelist: ShowBluffPanelist | None = Field(
        default=None, title="Correct Panelist"
    )


class ShowGuest(BaseModel):
    """Show Guest Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Guest ID")
    name: str = Field(title="Guest Name")
    slug: str | None = Field(default=None, title="Guest Slug String")
    score: int | None = Field(default=None, title="Guest Score")
    score_exception: bool = Field(default=False, title="Guest Scoring Exception")


class ShowDetails(Show):
    """Show Information, Host, Scorekeeper, Panelists, Guests and Additional Details."""

    location: ShowLocation | None = Field(default=None, title="Show Location")
    description: str | None = Field(default=None, title="Show Description")
    notes: str | None = Field(default=None, title="Show Notes (Plain Text or Markdown)")
    host: ShowHost | None = Field(default=None, title="Show Host")
    scorekeeper: ShowScorekeeper | None = Field(default=None, title="Show Scorekeeper")
    panelists: list[ShowPanelist] | None = Field(default=None, title="Show Panelists")
    bluffs: list[ShowBluffDetails] | None = Field(
        default=None, title="Bluff the Listener Information"
    )
    guests: list[ShowGuest] | None = Field(default=None, title="Show Guests")


class ShowsDetails(BaseModel):
    """List of Show Details."""

    shows: list[ShowDetails] = Field(
        title="List of Show Information and Additional Details"
    )


class ShowDates(BaseModel):
    """List of Show Dates in ISO format (YYYY-MM-DD)."""

    shows: list[str] = Field(title="List of Show Dates")
    shows: list[str] = Field(title="List of Show Dates")
