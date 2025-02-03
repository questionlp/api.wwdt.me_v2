# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/locations routes."""

import pytest
from fastapi.testclient import TestClient
from numpy import isin

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_locations():
    """Test /v2.0/locations route."""
    response = client.get(f"/v{API_VERSION}/locations")
    locations = response.json()

    assert response.status_code == 200
    assert "id" in locations["locations"][0]
    assert "slug" in locations["locations"][0]
    assert "venue" in locations["locations"][0]
    assert "city" in locations["locations"][0]
    assert "state" in locations["locations"][0]
    assert "coordinates" in locations["locations"][0]
    if locations["locations"][0]["coordinates"]:
        assert "latitude" in locations["locations"][0]["coordinates"]
        assert "longitude" in locations["locations"][0]["coordinates"]


@pytest.mark.parametrize("location_id", [32, 148])
def test_locations_id(location_id: int):
    """Test /v2.0/locations/id/{location_id} route."""
    response = client.get(f"/v{API_VERSION}/locations/id/{location_id}")
    location = response.json()

    assert response.status_code == 200
    assert "id" in location
    assert location["id"] == location_id
    assert "slug" in location
    assert "venue" in location
    assert "city" in location
    assert "state" in location
    assert "coordinates" in location
    if location["coordinates"]:
        assert "latitude" in location["coordinates"]
        assert "longitude" in location["coordinates"]


@pytest.mark.parametrize(
    "location_slug",
    ["arlene-schnitzer-concert-hall-portland-or", "home-remote-studios"],
)
def test_locations_slug(location_slug: str):
    """Test /v2.0/locations/slug/{location_slug} route."""
    response = client.get(f"/v{API_VERSION}/locations/slug/{location_slug}")
    location = response.json()

    assert response.status_code == 200
    assert "id" in location
    assert "slug" in location
    assert location["slug"] == location_slug
    assert "venue" in location
    assert "city" in location
    assert "state" in location
    if location["coordinates"]:
        assert "latitude" in location["coordinates"]
        assert "longitude" in location["coordinates"]


def test_locations_recordings():
    """Test /v2.0/locations/recordings route."""
    response = client.get(f"/v{API_VERSION}/locations/recordings")
    locations = response.json()

    assert response.status_code == 200
    assert "locations" in locations
    assert "id" in locations["locations"][0]
    assert "slug" in locations["locations"][0]
    assert "venue" in locations["locations"][0]
    assert "city" in locations["locations"][0]
    assert "state" in locations["locations"][0]
    assert "coordinates" in locations["locations"][0]
    if locations["locations"][0]["coordinates"]:
        assert "latitude" in locations["locations"][0]["coordinates"]
        assert "longitude" in locations["locations"][0]["coordinates"]
    assert "recordings" in locations["locations"][0]


@pytest.mark.parametrize("location_id", [32, 148])
def test_locations_recordings_id(location_id: int):
    """Test /v2.0/locations/recordings/id/{location_id} route."""
    response = client.get(f"/v{API_VERSION}/locations/recordings/id/{location_id}")
    location = response.json()

    assert response.status_code == 200
    assert "id" in location
    assert location["id"] == location_id
    assert "slug" in location
    assert "venue" in location
    assert "city" in location
    assert "state" in location
    if location["coordinates"]:
        assert "latitude" in location["coordinates"]
        assert "longitude" in location["coordinates"]
    assert "recordings" in location


@pytest.mark.parametrize(
    "location_slug",
    ["arlene-schnitzer-concert-hall-portland-or", "home-remote-studios"],
)
def test_locations_recordings_slug(location_slug: str):
    """Test /v2.0/locations/recordings/slug/{location_slug} route."""
    response = client.get(f"/v{API_VERSION}/locations/recordings/slug/{location_slug}")
    location = response.json()

    assert response.status_code == 200
    assert "id" in location
    assert "slug" in location
    assert location["slug"] == location_slug
    assert "venue" in location
    assert "city" in location
    assert "state" in location
    if location["coordinates"]:
        assert "latitude" in location["coordinates"]
        assert "longitude" in location["coordinates"]
    assert "recordings" in location


def test_locations_postal_abbreviations():
    """Test /v2.0/locations/postal-abbreviations route."""
    response = client.get(f"/v{API_VERSION}/locations/postal-abbreviations")
    abbreviations = response.json()

    assert response.status_code == 200
    assert isinstance(abbreviations, list)
    assert isinstance(abbreviations[0], str)


def test_locations_postal_abbreviations_details_all():
    """Test /v2.0/locations/postal-abbreviations/details route."""
    response = client.get(f"/v{API_VERSION}/locations/postal-abbreviations/details")
    abbreviations = response.json()

    assert response.status_code == 200
    assert "postal_abbreviations" in abbreviations
    assert isinstance(abbreviations["postal_abbreviations"], list)
    assert isinstance(abbreviations["postal_abbreviations"][0], dict)
    assert "postal_abbreviation" in abbreviations["postal_abbreviations"][0]
    assert "name" in abbreviations["postal_abbreviations"][0]
    assert "country" in abbreviations["postal_abbreviations"][0]


@pytest.mark.parametrize("abbreviation", ["OR", "DC"])
def test_locations_postal_abbreviations_details(abbreviation: str):
    """Test /v2.0/locations/postal-abbreviations/details route."""
    response = client.get(
        f"/v{API_VERSION}/locations/postal-abbreviations/details/{abbreviation}"
    )
    info = response.json()

    assert response.status_code == 200
    assert isinstance(info, dict)
    assert "postal_abbreviation" in info
    assert "name" in info
    assert "country" in info


def test_locations_random():
    """Test /v2.0/locations/random route."""
    response = client.get(f"/v{API_VERSION}/locations/random")
    location = response.json()

    assert response.status_code == 200
    assert "id" in location
    assert "venue" in location
    assert "slug" in location


def test_locations_random_details():
    """Test /v2.0/locations/recordings/random route."""
    response = client.get(f"/v{API_VERSION}/locations/recordings/random")
    location = response.json()

    assert response.status_code == 200
    assert "id" in location
    assert "venue" in location
    assert "slug" in location
    assert "recordings" in location


def test_locations_random_id():
    """Test /v2.0/locations/random/id route."""
    response = client.get(f"/v{API_VERSION}/locations/random/id")
    _id = response.json()

    assert response.status_code == 200
    assert "id" in _id
    assert isinstance(_id["id"], int)


def test_locations_random_slug():
    """Test /v2.0/locations/random/slug route."""
    response = client.get(f"/v{API_VERSION}/locations/random/slug")
    _slug = response.json()

    assert response.status_code == 200
    assert "slug" in _slug
    assert isinstance(_slug["slug"], str)
