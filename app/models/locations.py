# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Locations Models"""

from typing import List, Optional
from pydantic import BaseModel, conint, Field


# region Location Models
class Location(BaseModel):
    """Location Information"""
    id: conint(ge=0, lt=2**31) = Field(title="Location ID")
    city: Optional[str] = Field(default=None,
                                title="City")
    state: Optional[str] = Field(default=None,
                                 title="State")
    venue: Optional[str] = Field(default=None,
                                 title="Venue Name")
    slug: Optional[str] = Field(default=None,
                                title="Location Slug String")


class Locations(BaseModel):
    """List of Locations"""
    locations: List[Location] = Field(title="List of Locations")


class LocationRecordingCounts(BaseModel):
    """Count of Recordings for a Location"""
    regular_shows: Optional[int] = Field(default=None,
                                         title="Count of Regular Show Recordings")
    all_shows: Optional[int] = Field(default=None,
                                     title="Count of All Show Recordings")


class LocationRecordingShow(BaseModel):
    """Location Recording Information"""
    show_id: conint(ge=0, lt=2**31) = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")


class LocationRecordings(BaseModel):
    """Loation Information and Recordings"""
    count: Optional[LocationRecordingCounts] = Field(default=None,
                                                     title="Count of Show Recordings")
    shows: Optional[List[LocationRecordingShow]] = Field(default=None,
                                                         title="List of Show Recordings")


class LocationDetails(Location):
    """Location Information with Recordings"""
    recordings: Optional[LocationRecordings] = Field(default=None,
                                                     title="List of Show Recordings")


class LocationsDetails(BaseModel):
    """List of Location Details"""
    locations: List[LocationDetails] = Field(title="List of Location Details")

# endregion
