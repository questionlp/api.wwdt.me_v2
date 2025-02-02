# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Locations Models."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, RootModel


class LocationCoordinates(BaseModel):
    """Coordinates for a Location."""

    latitude: Decimal | None = Field(default=None, title="Venue Latitude")
    longitude: Decimal | None = Field(default=None, title="Venue Longitude")


class Location(BaseModel):
    """Location Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Location ID")
    city: str | None = Field(default=None, title="City")
    state: str | None = Field(default=None, title="State")
    venue: str | None = Field(default=None, title="Venue Name")
    coordinates: LocationCoordinates | None = Field(
        default=None, title="Location Coordinates"
    )
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


class LocationID(BaseModel):
    """Location ID."""

    id: int = Field(title="Location ID")


class LocationSlug(BaseModel):
    """Location Slug String."""

    slug: str = Field(title="Location Slug String")


class PostalAbbreviationDetails(BaseModel):
    """Postal Abbreviation Details."""

    postal_abbreviation: str = Field("Postal Abbreviation")
    name: str = Field(title="State, Province or Territory Name")
    country: str = Field(title="Country Name")


class PostalAbbreviations(RootModel[list[str]]):
    """List of Postal Abbreviations."""


class PostalAbbreviationsDetails(BaseModel):
    """List of Postal Abbreviations Details."""

    postal_abbreviations: list[PostalAbbreviationDetails] = Field(
        "List of Postal Abbreviations Details"
    )
