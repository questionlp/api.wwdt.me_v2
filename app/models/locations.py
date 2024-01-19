# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Locations Models."""

from typing import Annotated

from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Location ID")
    city: str | None = Field(default=None, title="City")
    state: str | None = Field(default=None, title="State")
    venue: str | None = Field(default=None, title="Venue Name")
    slug: str | None = Field(default=None, title="Location Slug String")


class Locations(BaseModel):
    """List of Locations."""

    locations: list[Location] = Field(title="List of Locations")


class LocationRecordingCounts(BaseModel):
    """Count of Recordings for a Location."""

    regular_shows: int | None = Field(
        default=None, title="Count of Regular Show Recordings"
    )
    all_shows: int | None = Field(default=None, title="Count of All Show Recordings")


class LocationRecordingShow(BaseModel):
    """Location Recording Information."""

    show_id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")


class LocationRecordings(BaseModel):
    """Location Information and Recordings."""

    count: LocationRecordingCounts | None = Field(
        default=None, title="Count of Show Recordings"
    )
    shows: list[LocationRecordingShow] | None = Field(
        default=None, title="List of Show Recordings"
    )


class LocationDetails(Location):
    """Location Information with Recordings."""

    recordings: LocationRecordings | None = Field(
        default=None, title="List of Show Recordings"
    )


class LocationsDetails(BaseModel):
    """List of Location Details."""

    locations: list[LocationDetails] = Field(title="List of Location Details")
    locations: list[LocationDetails] = Field(title="List of Location Details")
