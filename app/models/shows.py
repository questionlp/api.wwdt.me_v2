# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Shows Models"""

from typing import List, Optional, Union
from pydantic import BaseModel, conint, Field


class Show(BaseModel):
    """Show Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Best Of Show")


class Shows(BaseModel):
    """List of Shows"""

    shows: List[Show] = Field(title="List of Shows")


class ShowLocation(BaseModel):
    """Show Location Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Location ID")
    slug: Optional[str] = Field(default=None, title="Location Slug String")
    city: Optional[str] = Field(default=None, title="City")
    state: Optional[str] = Field(default=None, title="State")
    venue: Optional[str] = Field(default=None, title="Venue Name")


class ShowHost(BaseModel):
    """Show Host Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Host ID")
    name: str = Field(title="Host Name")
    slug: Optional[str] = Field(default=None, title="Host Slug String")
    guest: bool = Field(title="Guest Host")


class ShowScorekeeper(BaseModel):
    """Show Scorekeeper Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Scorekeeper ID")
    name: str = Field(title="Scorekeeper Name")
    slug: Optional[str] = Field(default=None, title="Scorekeeper Slug String")
    guest: bool = Field(title="Guest Scorekeeper")
    description: Optional[str] = Field(default=None, title="Scorekeeper Description")


class ShowPanelist(BaseModel):
    """Show Panelist Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: Optional[str] = Field(default=None, title="Panelist Slug String")
    lightning_round_start: Union[int, None] = Field(
        default=None, title="Lightning Fill-in-the-Blank Starting Score"
    )
    lightning_round_correct: Union[int, None] = Field(
        default=None, title="Lightning Fill-in-the-Blank Corect Answers"
    )
    score: Union[int, None] = Field(default=None, title="Panelist Score")
    rank: Union[str, None] = Field(default=None, title="Panelist Rank")


class ShowBluffPanelist(BaseModel):
    """Show Bluff the Listener Panelist Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: Optional[str] = Field(default=None, title="Panelist Slug String")


class ShowBluffDetails(BaseModel):
    """Show Bluff the Listener Chosen and Correct Panelists"""

    chosen_panelist: Optional[ShowBluffPanelist] = Field(
        default=None, title="Chosen Panelist"
    )
    correct_panelist: Optional[ShowBluffPanelist] = Field(
        default=None, title="Correct Panelist"
    )


class ShowGuest(BaseModel):
    """Show Guest Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Guest ID")
    name: str = Field(title="Guest Name")
    slug: Optional[str] = Field(default=None, title="Guest Slug String")
    score: Union[int, None] = Field(default=None, title="Guest Score")
    score_exception: bool = Field(default=False, title="Guest Scoring Exception")


class ShowDetails(Show):
    """Show Information, Host, Scorekeeper, Panelists, Guests and
    Additional Details"""

    location: Optional[ShowLocation] = Field(title="Show Location")
    description: Optional[str] = Field(default=None, title="Show Description")
    notes: Optional[str] = Field(
        default=None, title="Show Notes (Plain Text or Markdown)"
    )
    host: Optional[ShowHost] = Field(default=None, title="Show Host")
    scorekeeper: Optional[ShowScorekeeper] = Field(
        default=None, title="Show Scorekeeper"
    )
    panelists: Optional[List[ShowPanelist]] = Field(
        default=None, title="Show Panelists"
    )
    bluff: Optional[ShowBluffDetails] = Field(
        default=None, title="Bluff the Listener Information"
    )
    guests: Optional[List[ShowGuest]] = Field(default=None, title="Show Guests")


class ShowsDetails(BaseModel):
    """List of Show Details"""

    shows: List[ShowDetails] = Field(
        title="List of Show Information and Additional Details"
    )


class ShowDates(BaseModel):
    """List of Show Dates in ISO format (YYYY-MM-DD)"""

    shows: List[str] = Field(title="List of Show Dates")
