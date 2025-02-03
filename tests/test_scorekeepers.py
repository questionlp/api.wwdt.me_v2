# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/scorekeepers routes."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_scorekeepers():
    """Test /v2.0/scorekeepers route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers")
    scorekeepers = response.json()

    assert response.status_code == 200
    assert "scorekeepers" in scorekeepers
    assert "id" in scorekeepers["scorekeepers"][0]
    assert "name" in scorekeepers["scorekeepers"][0]
    assert "pronouns" in scorekeepers["scorekeepers"][0]
    assert "slug" in scorekeepers["scorekeepers"][0]


@pytest.mark.parametrize("scorekeeper_id", [11])
def test_scorekeepers_id(scorekeeper_id: int):
    """Test /v2.0/scorekeepers/id/{scorekeeper_id} route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/id/{scorekeeper_id}")
    scorekeeper = response.json()

    assert response.status_code == 200
    assert "id" in scorekeeper
    assert scorekeeper["id"] == scorekeeper_id
    assert "name" in scorekeeper
    assert "pronouns" in scorekeeper
    assert "slug" in scorekeeper


@pytest.mark.parametrize("scorekeeper_slug", ["bill-kurtis"])
def test_scorekeepers_slug(scorekeeper_slug: str):
    """Test /v2.0/scorekeepers/slug/{scorekeeper_slug} route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/slug/{scorekeeper_slug}")
    scorekeeper = response.json()

    assert response.status_code == 200
    assert "id" in scorekeeper
    assert "name" in scorekeeper
    assert "pronouns" in scorekeeper
    assert "slug" in scorekeeper
    assert scorekeeper["slug"] == scorekeeper_slug


def test_scorekeepers_details():
    """Test /v2.0/scorekeepers/details route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/details")
    scorekeepers = response.json()

    assert response.status_code == 200
    assert "scorekeepers" in scorekeepers
    assert "id" in scorekeepers["scorekeepers"][0]
    assert "name" in scorekeepers["scorekeepers"][0]
    assert "pronouns" in scorekeepers["scorekeepers"][0]
    assert "slug" in scorekeepers["scorekeepers"][0]
    assert "appearances" in scorekeepers["scorekeepers"][0]


@pytest.mark.parametrize("scorekeeper_id", [11])
def test_scorekeepers_details_id(scorekeeper_id: int):
    """Test /v2.0/scorekeepers/details/id/{scorekeeper_id} route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/details/id/{scorekeeper_id}")
    scorekeeper = response.json()

    assert response.status_code == 200
    assert "id" in scorekeeper
    assert scorekeeper["id"] == scorekeeper_id
    assert "name" in scorekeeper
    assert "pronouns" in scorekeeper
    assert "slug" in scorekeeper
    assert "appearances" in scorekeeper


@pytest.mark.parametrize("scorekeeper_slug", ["bill-kurtis"])
def test_scorekeepers_details_slug(scorekeeper_slug: str):
    """Test /v2.0/scorekeepers/details/slug/{scorekeeper_slug} route."""
    response = client.get(
        f"/v{API_VERSION}/scorekeepers/details/slug/{scorekeeper_slug}"
    )
    scorekeeper = response.json()

    assert response.status_code == 200
    assert "id" in scorekeeper
    assert "name" in scorekeeper
    assert "pronouns" in scorekeeper
    assert "slug" in scorekeeper
    assert scorekeeper["slug"] == scorekeeper_slug
    assert "appearances" in scorekeeper


def test_scorekeepers_random():
    """Test /v2.0/scorekeepers/random route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/random")
    scorekeeper = response.json()

    assert response.status_code == 200
    assert "id" in scorekeeper
    assert "name" in scorekeeper
    assert "pronouns" in scorekeeper
    assert "slug" in scorekeeper


def test_scorekeepers_random_details():
    """Test /v2.0/scorekeepers/details/random route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/details/random")
    scorekeeper = response.json()

    assert response.status_code == 200
    assert "id" in scorekeeper
    assert "name" in scorekeeper
    assert "pronouns" in scorekeeper
    assert "slug" in scorekeeper
    assert "appearances" in scorekeeper


def test_scorekeepers_random_id():
    """Test /v2.0/scorekeepers/random/id route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/random/id")
    _id = response.json()

    assert response.status_code == 200
    assert "id" in _id
    assert isinstance(_id["id"], int)


def test_scorekeepers_random_slug():
    """Test /v2.0/scorekeepers/random/slug route."""
    response = client.get(f"/v{API_VERSION}/scorekeepers/random/slug")
    _slug = response.json()

    assert response.status_code == 200
    assert "slug" in _slug
    assert isinstance(_slug["slug"], str)
