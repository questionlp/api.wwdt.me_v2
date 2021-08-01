# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""Hosts Models"""

from typing import List, Optional, Union
from pydantic import BaseModel, Field, PositiveInt

#region Host Models
class Host(BaseModel):
    """Host Information"""
    id: PositiveInt = Field(title="Host ID")
    name: str = Field(title="Host Name")
    slug: Optional[str] = Field(default=None,
                                title="Host Slug String")
    gender: Optional[str] = Field(default=None,
                                  title="Host Gender")

class Hosts(BaseModel):
    """List of Hosts"""
    hosts: List[Host] = Field(title="List of Hosts")

class HostAppearanceCounts(BaseModel):
    """Count of Show Appearances"""
    regular_shows: Optional[int] = Field(default=None,
                                         title="Count of Regular Show Appearances")
    all_shows: Optional[int] = Field(default=None,
                                     title="Count of All Show Appearances")

class HostAppearance(BaseModel):
    """Appearance Information"""
    show_id: PositiveInt = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    guest: bool = Field(title="Guest Host")

class HostAppearances(BaseModel):
    """Host Appearance Information"""
    count: Union[HostAppearanceCounts, int] = Field(title="Count of Show Appearances")
    shows: Optional[List[HostAppearance]] = Field(default=None,
                                                  title="List of Show Appearances")

class HostDetails(Host):
    """Host Information with Appearances"""
    appearances: Optional[HostAppearances] = Field(default=None,
                                                   title="List of Show Appearances")

class HostsDetails(BaseModel):
    """List of Host Details"""
    hosts: List[HostDetails] = Field(title="List of Host Details")

#endregion
