# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""Shows Models"""

from typing import List, Optional
from pydantic import BaseModel, Field, PositiveInt

#region Shows Models
class Show(BaseModel):
    """Show Information"""
    id: PositiveInt = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Best Of Show")

class Shows(BaseModel):
    """List of Shows"""
    shows: List[Show] = Field(title="List of Shows")

class ShowLocation(BaseModel):
    """Show Location Information"""
    id: PositiveInt = Field(title="Location ID")
    slug: Optional[str] = Field(default=None,
                                title="Location Slug String")
    city: Optional[str] = Field(default=None,
                                title="City")
    state: Optional[str] = Field(default=None,
                                 title="State")
    venue: Optional[str] = Field(default=None,
                                 title="Venue Name")

class ShowHost(BaseModel):
    """Show Host Information"""
    id: PositiveInt = Field(title="Host ID")
    name: str = Field(title="Host Name")
    slug: Optional[str] = Field(default=None,
                                title="Host Slug String")
    guest: bool = Field(title="Guest Host")

class ShowScorekeeper(BaseModel):
    """Show Scorekeeper Information"""
    id: PositiveInt = Field(title="Scorekeeper ID")
    name: str = Field(title="Scorekeeper Name")
    slug: Optional[str] = Field(default=None,
                                title="Scorekeeper Slug String")
    description: Optional[str] = Field(default=None,
                                       title="Scorekeeper Description")

class ShowPanelist(BaseModel):
    """Show Panelist Information"""
    id: PositiveInt = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: Optional[str] = Field(default=None,
                                title="Panelist Slug String")
    lightning_round_start: Optional[int] = Field(default=None,
                                                 title="Lightning Fill-in-the-Blank Starting Score")
    lightning_round_correct: Optional[int] = Field(default=None,
                                                   title="Lightning Fill-in-the-Blank Corect Answers")
    score: Optional[int] = Field(default=None,
                                 title="Panelist Score")
    rank: Optional[str] = Field(default=None,
                                title="Panelist Rank")

class ShowBluffPanelist(BaseModel):
    """Show Bluff the Listener Panelist Information"""
    id: PositiveInt = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: Optional[str] = Field(default=None,
                                title="Panelist Slug String")

class ShowBluffDetails(BaseModel):
    """Show Bluff the Listener Chosen and Correct Panelists"""
    chosen_panelist: Optional[ShowBluffPanelist] = Field(default=None,
                                                         title="Chosen Panelist")
    correct_panelist: Optional[ShowBluffPanelist] = Field(default=None,
                                                          title="Correct Panelist")

class ShowGuest(BaseModel):
    """Show Guest Information"""
    id: PositiveInt = Field(title="Guest ID")
    name: str = Field(title="Guest Name")
    slug: Optional[str] = Field(default=None,
                                title="Guest Slug String")
    score: Optional[int] = Field(default=None,
                                 title="Guest Score")
    score_exception: Optional[bool] = Field(default=None,
                                            title="Guest Scoring Exception")

class ShowDetails(Show):
    """Show Information, Host, Scorekeeper, Panelists, Guests and
    Additional Details"""
    location: Optional[ShowLocation] = Field(title="Show Location")
    description: Optional[str] = Field(default=None,
                                       title="Show Description")
    notes: Optional[str] = Field(default=None,
                                 title="Show Notes")
    host: Optional[ShowHost] = Field(default=None,
                                     title="Show Host")
    scorekeeper: Optional[ShowScorekeeper] = Field(default=None,
                                                   title="Show Scorekeeper")
    panelists: Optional[List[ShowPanelist]] = Field(default=None,
                                                    title="Show Panelists")
    bluff: Optional[ShowBluffDetails] = Field(default=None,
                                              title="Bluff the Listener Information")
    guests: Optional[List[ShowGuest]] = Field(default=None,
                                              title="Show Guests")

class ShowsDetails(BaseModel):
    """List of Show Details"""
    shows: List[ShowDetails] = Field(title="List of Show Information and Additional Details")

#endregion
