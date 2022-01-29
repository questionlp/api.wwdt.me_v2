# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Scorekeepers Models"""

from typing import List, Optional, Union
from pydantic import BaseModel, conint, Field


# region Scorekeeper Models
class Scorekeeper(BaseModel):
    """Scorekeeper Information"""
    id: conint(ge=0, lt=2**31) = Field(title="Scorekeeper ID")
    name: str = Field(title="Scorekeeper Name")
    slug: Optional[str] = Field(default=None,
                                title="Scorekeeper Slug String")
    gender: Optional[str] = Field(default=None,
                                  title="Scorekeeper Gender")


class Scorekeepers(BaseModel):
    """List of Scorekeepers"""
    scorekeepers: List[Scorekeeper] = Field(title="List of Scorekeepers")


class ScorekeeperAppearanceCounts(BaseModel):
    """Count of Show Appearances"""
    regular_shows: Optional[int] = Field(default=None,
                                         title="Count of Regular Show Appearances")
    all_shows: Optional[int] = Field(default=None,
                                     title="Count of All Show Appearances")


class ScorekeeperAppearance(BaseModel):
    """Appearance Information"""
    show_id: conint(ge=0, lt=2**31) = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    guest: bool = Field(title="Guest Scorekeeper")
    description: Optional[str] = Field(default=None,
                                       title="Scorekeeper Introduction")


class ScorekeeperAppearances(BaseModel):
    """Scorekeeper Appearance Information"""
    count: Union[ScorekeeperAppearanceCounts, int] = Field(title="Count of Show Appearances")
    shows: Optional[List[ScorekeeperAppearance]] = Field(default=None,
                                                         title="List of Show Appearances")


class ScorekeeperDetails(Scorekeeper):
    """Scorekeeper Information with Appearances"""
    appearances: Optional[ScorekeeperAppearances] = Field(default=None,
                                                          title="List of Show Appearances")


class ScorekeepersDetails(BaseModel):
    """List of Scorekeeper Details"""
    scorekeepers: List[ScorekeeperDetails] = Field(title="List of Scorekeeper Details")

# endregion
