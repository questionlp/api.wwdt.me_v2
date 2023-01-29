# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Guests Models"""

from typing import List, Optional, Union
from pydantic import BaseModel, conint, Field


class Guest(BaseModel):
    """Not My Job Guest Information"""

    id: conint(ge=0, lt=2**31) = Field(title="Guest ID")
    name: str = Field(title="Guest Name")
    slug: Optional[str] = Field(default=None, title="Guest Slug String")


class Guests(BaseModel):
    """List of Not My Job Guests"""

    guests: List[Guest] = Field(title="List of Guests")


class GuestAppearanceCounts(BaseModel):
    """Count of Show Appearances"""

    regular_shows: Optional[int] = Field(
        default=None, title="Count of Regular Show Appearances"
    )
    all_shows: Optional[int] = Field(
        default=None, title="Count of All Show Appearances"
    )


class GuestAppearance(BaseModel):
    """Appearance Information"""

    show_id: conint(ge=0, lt=2**31) = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    score: Optional[int] = Field(default=None, title="Guest Score")
    score_exception: Optional[bool] = Field(
        default=None, title="Guest Scoring Exception"
    )


class GuestAppearances(BaseModel):
    """Not My Job Guest Appearances Information"""

    count: Union[GuestAppearanceCounts, int] = Field(title="Count of Show Appearances")
    shows: Optional[List[GuestAppearance]] = Field(
        default=None, title="List of Show Appearances"
    )


class GuestDetails(Guest):
    """Not My Job Guest Information with Appearances"""

    appearances: Optional[GuestAppearances] = Field(
        default=None, title="List of Show Appearances"
    )


class GuestsDetails(BaseModel):
    """List of Not My Job Guest Details"""

    guests: List[GuestDetails] = Field(title="List of Guest Details")
