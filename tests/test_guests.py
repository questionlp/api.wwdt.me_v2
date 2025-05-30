# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/guests routes."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_get_guests():
    """Test /v2.0/guests route."""
    response = client.get(f"/v{API_VERSION}/guests")
    guests = response.json()

    assert response.status_code == 200
    assert "guests" in guests
    assert "id" in guests["guests"][0]
    assert "name" in guests["guests"][0]
    assert "slug" in guests["guests"][0]


@pytest.mark.parametrize("guest_id", [54])
def test_get_guest_by_id(guest_id: int):
    """Test /v2.0/guests/id/{guest_id} route."""
    response = client.get(f"/v{API_VERSION}/guests/id/{guest_id}")
    guest = response.json()

    assert response.status_code == 200
    assert "id" in guest
    assert guest["id"] == guest_id
    assert "name" in guest
    assert "slug" in guest


@pytest.mark.parametrize("guest_id", [0])
def test_get_guest_by_id_not_found(guest_id: int):
    """Test /v2.0/guests/id/{guest_id} route."""
    response = client.get(f"/v{API_VERSION}/guests/id/{guest_id}")
    guest = response.json()

    assert response.status_code == 404
    assert "detail" in guest


@pytest.mark.parametrize("guest_slug", ["tom-hanks"])
def test_get_guest_by_slug(guest_slug: str):
    """Test /v2.0/guests/slug/{guest_slug} route."""
    response = client.get(f"/v{API_VERSION}/guests/slug/{guest_slug}")
    guest = response.json()

    assert response.status_code == 200
    assert "id" in guest
    assert "name" in guest
    assert "slug" in guest
    assert guest["slug"] == guest_slug


@pytest.mark.parametrize("guest_slug", ["-abcdef"])
def test_get_guest_by_slug_not_found(guest_slug: str):
    """Test /v2.0/guests/slug/{guest_slug} route."""
    response = client.get(f"/v{API_VERSION}/guests/slug/{guest_slug}")
    guest = response.json()

    assert response.status_code == 404
    assert "detail" in guest


def test_get_guests_details():
    """Test /v2.0/guests/details route."""
    response = client.get(f"/v{API_VERSION}/guests/details")
    guests = response.json()

    assert response.status_code == 200
    assert "guests" in guests
    assert "id" in guests["guests"][0]
    assert "name" in guests["guests"][0]
    assert "slug" in guests["guests"][0]
    assert "appearances" in guests["guests"][0]


@pytest.mark.parametrize("guest_id", [54])
def test_get_guest_details_by_id(guest_id: int):
    """Test /v2.0/guests/details/id/{guest_id} route."""
    response = client.get(f"/v{API_VERSION}/guests/details/id/{guest_id}")
    guest = response.json()

    assert response.status_code == 200
    assert "id" in guest
    assert guest["id"] == guest_id
    assert "name" in guest
    assert "slug" in guest
    assert "appearances" in guest


@pytest.mark.parametrize("guest_id", [0])
def test_get_guest_details_by_id_not_found(guest_id: int):
    """Test /v2.0/guests/details/id/{guest_id} route."""
    response = client.get(f"/v{API_VERSION}/guests/details/id/{guest_id}")
    guest = response.json()

    assert response.status_code == 404
    assert "detail" in guest


def test_get_random_guest_details():
    """Test /v2.0/guests/details/random route."""
    response = client.get(f"/v{API_VERSION}/guests/details/random")
    guest = response.json()

    assert response.status_code == 200
    assert "id" in guest
    assert "name" in guest
    assert "slug" in guest
    assert "appearances" in guest


@pytest.mark.parametrize("guest_slug", ["tom-hanks"])
def test_get_guest_details_by_slug(guest_slug: str):
    """Test /v2.0/guests/details/slug/{guest_slug} route."""
    response = client.get(f"/v{API_VERSION}/guests/details/slug/{guest_slug}")
    guest = response.json()

    assert response.status_code == 200
    assert "id" in guest
    assert "name" in guest
    assert "slug" in guest
    assert guest["slug"] == guest_slug
    assert "appearances" in guest


@pytest.mark.parametrize("guest_slug", ["-abcdef"])
def test_get_guest_details_by_slug_not_found(guest_slug: str):
    """Test /v2.0/guests/details/slug/{guest_slug} route."""
    response = client.get(f"/v{API_VERSION}/guests/details/slug/{guest_slug}")
    guest = response.json()

    assert response.status_code == 404
    assert "detail" in guest


def test_get_random_guest():
    """Test /v2.0/guests/random route."""
    response = client.get(f"/v{API_VERSION}/guests/random")
    guest = response.json()

    assert response.status_code == 200
    assert "id" in guest
    assert "name" in guest
    assert "slug" in guest


def test_get_random_guest_id():
    """Test /v2.0/guests/random/id route."""
    response = client.get(f"/v{API_VERSION}/guests/random/id")
    _id = response.json()

    assert response.status_code == 200
    assert "id" in _id
    assert isinstance(_id["id"], int)


def test_get_randon_guest_slug():
    """Test /v2.0/guests/random/slug route."""
    response = client.get(f"/v{API_VERSION}/guests/random/slug")
    _slug = response.json()

    assert response.status_code == 200
    assert "slug" in _slug
    assert isinstance(_slug["slug"], str)
