# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/panelists routes."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_get_panelists():
    """Test /v2.0/panelists route."""
    response = client.get(f"/v{API_VERSION}/panelists")
    panelists = response.json()

    assert response.status_code == 200
    assert "panelists" in panelists
    assert "id" in panelists["panelists"][0]
    assert "name" in panelists["panelists"][0]
    assert "pronouns" in panelists["panelists"][0]
    assert "slug" in panelists["panelists"][0]


@pytest.mark.parametrize("panelist_id", [30])
def test_get_panelist_by_id(panelist_id: int):
    """Test /v2.0/panelists/id/{panelist_id} route."""
    response = client.get(f"/v{API_VERSION}/panelists/id/{panelist_id}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert panelist["id"] == panelist_id
    assert "name" in panelist
    assert "pronouns" in panelist
    assert "slug" in panelist


@pytest.mark.parametrize("panelist_id", [0])
def test_get_panelist_by_id_not_found(panelist_id: int):
    """Test /v2.0/panelists/id/{panelist_id} route."""
    response = client.get(f"/v{API_VERSION}/panelists/id/{panelist_id}")
    panelist = response.json()

    assert response.status_code == 404
    assert "detail" in panelist


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_get_panelist_by_slug(panelist_slug: str):
    """Test /v2.0/panelists/slug/{panelist_slug} route."""
    response = client.get(f"/v{API_VERSION}/panelists/slug/{panelist_slug}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert "name" in panelist
    assert "pronouns" in panelist
    assert "slug" in panelist
    assert panelist["slug"] == panelist_slug


@pytest.mark.parametrize("panelist_slug", ["-abcdef"])
def test_get_panelist_by_slug_not_found(panelist_slug: str):
    """Test /v2.0/panelists/slug/{panelist_slug} route."""
    response = client.get(f"/v{API_VERSION}/panelists/slug/{panelist_slug}")
    panelist = response.json()

    assert response.status_code == 404
    assert "detail" in panelist


def test_get_panelists_details():
    """Test /v2.0/panelists/details route."""
    response = client.get(f"/v{API_VERSION}/panelists/details")
    panelists = response.json()

    assert response.status_code == 200
    assert "panelists" in panelists
    assert "id" in panelists["panelists"][0]
    assert "name" in panelists["panelists"][0]
    assert "pronouns" in panelists["panelists"][0]
    assert "slug" in panelists["panelists"][0]
    assert "appearances" in panelists["panelists"][0]


@pytest.mark.parametrize("panelist_id", [30])
def test_get_panelist_details_by_id(panelist_id: int):
    """Test /v2.0/panelists/details/id/{panelist_id} route."""
    response = client.get(f"/v{API_VERSION}/panelists/details/id/{panelist_id}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert panelist["id"] == panelist_id
    assert "name" in panelist
    assert "pronouns" in panelist
    assert "slug" in panelist
    assert "appearances" in panelist


@pytest.mark.parametrize("panelist_id", [0])
def test_get_panelist_details_by_id_not_found(panelist_id: int):
    """Test /v2.0/panelists/details/id/{panelist_id} route."""
    response = client.get(f"/v{API_VERSION}/panelists/details/id/{panelist_id}")
    panelist = response.json()

    assert response.status_code == 404
    assert "detail" in panelist


def test_get_random_panelist_details():
    """Test /v2.0/panelists/details/random route."""
    response = client.get(f"/v{API_VERSION}/panelists/details/random")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert "name" in panelist
    assert "pronouns" in panelist
    assert "slug" in panelist
    assert "appearances" in panelist


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_get_panelist_details_by_slug(panelist_slug: str):
    """Test /v2.0/panelists/details/slug/{panelist_slug} route."""
    response = client.get(f"/v{API_VERSION}/panelists/details/slug/{panelist_slug}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert "name" in panelist
    assert "pronouns" in panelist
    assert "slug" in panelist
    assert panelist["slug"] == panelist_slug
    assert "appearances" in panelist


@pytest.mark.parametrize("panelist_slug", ["-abcdef"])
def test_get_panelist_details_by_slug_not_found(panelist_slug: str):
    """Test /v2.0/panelists/details/slug/{panelist_slug} route."""
    response = client.get(f"/v{API_VERSION}/panelists/details/slug/{panelist_slug}")
    panelist = response.json()

    assert response.status_code == 404
    assert "detail" in panelist


@pytest.mark.parametrize("panelist_id", [30])
def test_get_panelist_scores_by_id(panelist_id: int):
    """Test /v2.0/panelists/scores/id/{panelist_id} route."""
    response = client.get(f"/v{API_VERSION}/panelists/scores/id/{panelist_id}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_id", [0])
def test_get_panelist_scores_by_id_not_found(panelist_id: int):
    """Test /v2.0/panelists/scores/id/{panelist_id} route."""
    response = client.get(f"/v{API_VERSION}/panelists/scores/id/{panelist_id}")
    scores = response.json()

    assert response.status_code == 404
    assert "detail" in scores


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_get_panelist_scores_by_slug(panelist_slug: str):
    """Test /v2.0/panelists/scores/slug/{panelist_slug} route."""
    response = client.get(f"/v{API_VERSION}/panelists/scores/slug/{panelist_slug}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_slug", ["-abcdef"])
def test_get_panelist_scores_by_slug_not_found(panelist_slug: str):
    """Test /v2.0/panelists/scores/slug/{panelist_slug} route."""
    response = client.get(f"/v{API_VERSION}/panelists/scores/slug/{panelist_slug}")
    scores = response.json()

    assert response.status_code == 404
    assert "detail" in scores


@pytest.mark.parametrize("panelist_id", [30])
def test_get_panelist_scores_grouped_ordered_pair_by_id(panelist_id: int):
    """Test /v2.0/panelists/scores/grouped-ordered-pair/id/{panelist_id} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/grouped-ordered-pair/id/{panelist_id}"
    )
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_id", [0])
def test_get_panelist_scores_grouped_ordered_pair_by_id_not_found(panelist_id: int):
    """Test /v2.0/panelists/scores/grouped-ordered-pair/id/{panelist_id} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/grouped-ordered-pair/id/{panelist_id}"
    )
    scores = response.json()

    assert response.status_code == 404
    assert "detail" in scores


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_get_panelist_scores_grouped_ordered_pair_by_slug(panelist_slug: str):
    """Test /v2.0/panelists/scores/grouped-ordered-pair/slug/{panelist_slug} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/grouped-ordered-pair/slug/{panelist_slug}"
    )
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_slug", ["-abcdef"])
def test_get_panelist_scores_grouped_ordered_pair_by_slug_not_found(panelist_slug: str):
    """Test /v2.0/panelists/scores/grouped-ordered-pair/slug/{panelist_slug} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/grouped-ordered-pair/slug/{panelist_slug}"
    )
    scores = response.json()

    assert response.status_code == 404
    assert "detail" in scores


@pytest.mark.parametrize("panelist_id", [30])
def test_get_panelists_scores_ordered_pair_by_id(panelist_id: int):
    """Test /v2.0/panelists/scores/ordered-pair/id/{panelist_id} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/ordered-pair/id/{panelist_id}"
    )
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_id", [0])
def test_get_panelists_scores_ordered_pair_by_id_not_found(panelist_id: int):
    """Test /v2.0/panelists/scores/ordered-pair/id/{panelist_id} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/ordered-pair/id/{panelist_id}"
    )
    scores = response.json()

    assert response.status_code == 404
    assert "detail" in scores


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_get_panelists_scores_ordered_pair_by_slug(panelist_slug: str):
    """Test /v2.0/panelists/scores/ordered-pair/slug/{panelist_slug} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/ordered-pair/slug/{panelist_slug}"
    )
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_slug", ["-abcdef"])
def test_get_panelists_scores_ordered_pair_by_slug_not_found(panelist_slug: str):
    """Test /v2.0/panelists/scores/ordered-pair/slug/{panelist_slug} route."""
    response = client.get(
        f"/v{API_VERSION}/panelists/scores/ordered-pair/slug/{panelist_slug}"
    )
    scores = response.json()

    assert response.status_code == 404
    assert "detail" in scores


def test_get_random_panelist():
    """Test /v2.0/panelists/random route."""
    response = client.get(f"/v{API_VERSION}/panelists/random")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert "name" in panelist
    assert "pronouns" in panelist
    assert "slug" in panelist


def test_get_random_panelist_id():
    """Test /v2.0/panelists/random/id route."""
    response = client.get(f"/v{API_VERSION}/panelists/random/id")
    _id = response.json()

    assert response.status_code == 200
    assert "id" in _id
    assert isinstance(_id["id"], int)


def test_get_panelist_slug():
    """Test /v2.0/panelists/random/slug route."""
    response = client.get(f"/v{API_VERSION}/panelists/random/slug")
    _slug = response.json()

    assert response.status_code == 200
    assert "slug" in _slug
    assert isinstance(_slug["slug"], str)
