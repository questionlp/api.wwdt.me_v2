# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Testing /v2.0/panelists routes
"""
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.config import API_VERSION

client = TestClient(app)


def test_panelists():
    """Test /v2.0/panelists route"""

    response = client.get(f"/v{API_VERSION}/panelists")
    panelists = response.json()

    assert response.status_code == 200
    assert "panelists" in panelists
    assert "id" in panelists["panelists"][0]
    assert "name" in panelists["panelists"][0]
    assert "slug" in panelists["panelists"][0]


@pytest.mark.parametrize("panelist_id", [30])
def test_panelists_id(panelist_id: int):
    """Test /v2.0/panelists/id/{panelist_id} route"""

    response = client.get(f"/v{API_VERSION}/panelists/id/{panelist_id}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert panelist["id"] == panelist_id
    assert "name" in panelist
    assert "slug" in panelist


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelists_slug(panelist_slug: str):
    """Test /v2.0/panelists/slug/{panelist_slug} route"""

    response = client.get(f"/v{API_VERSION}/panelists/slug/{panelist_slug}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert "name" in panelist
    assert "slug" in panelist
    assert panelist["slug"] == panelist_slug


def test_panelists_details():
    """Test /v2.0/panelists/details route"""

    response = client.get(f"/v{API_VERSION}/panelists/details")
    panelists = response.json()

    assert response.status_code == 200
    assert "panelists" in panelists
    assert "id" in panelists["panelists"][0]
    assert "name" in panelists["panelists"][0]
    assert "slug" in panelists["panelists"][0]
    assert "appearances" in panelists["panelists"][0]


@pytest.mark.parametrize("panelist_id", [30])
def test_panelists_details_id(panelist_id: int):
    """Test /v2.0/panelists/details/id/{panelist_id} route"""

    response = client.get(f"/v{API_VERSION}/panelists/details/id/{panelist_id}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert panelist["id"] == panelist_id
    assert "name" in panelist
    assert "slug" in panelist
    assert "appearances" in panelist


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelists_details_slug(panelist_slug: str):
    """Test /v2.0/panelists/details/slug/{panelist_slug} route"""

    response = client.get(f"/v{API_VERSION}/panelists/details/slug/{panelist_slug}")
    panelist = response.json()

    assert response.status_code == 200
    assert "id" in panelist
    assert "name" in panelist
    assert "slug" in panelist
    assert panelist["slug"] == panelist_slug
    assert "appearances" in panelist


@pytest.mark.parametrize("panelist_id", [30])
def test_panelists_scores_id(panelist_id: int):
    """Test /v2.0/panelists/scores/id/{panelist_id} route"""

    response = client.get(f"/v{API_VERSION}/panelists/scores/id/{panelist_id}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores



@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelists_scores_slug(panelist_slug: str):
    """Test /v2.0/panelists/scores/slug/{panelist_slug} route"""

    response = client.get(f"/v{API_VERSION}/panelists/scores/slug/{panelist_slug}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_id", [30])
def test_panelists_scores_ordered_pair_id(panelist_id: int):
    """Test /v2.0/panelists/scores/ordered-pair/id/{panelist_id} route"""

    response = client.get(f"/v{API_VERSION}/panelists/scores/ordered-pair/id/{panelist_id}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelists_scores_ordered_pair_slug(panelist_slug: str):
    """Test /v2.0/panelists/scores/ordered-pair/slug/{panelist_slug} route"""

    response = client.get(f"/v{API_VERSION}/panelists/scores/ordered-pair/slug/{panelist_slug}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_id", [30])
def test_panelists_scores_grouped_ordered_pair_id(panelist_id: int):
    """Test /v2.0/panelists/scores/grouped-ordered-pair/id/{panelist_id} route"""

    response = client.get(f"/v{API_VERSION}/panelists/scores/grouped-ordered-pair/id/{panelist_id}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelists_scores_grouped_ordered_pair_slug(panelist_slug: str):
    """Test /v2.0/panelists/scores/grouped-ordered-pair/slug/{panelist_slug} route"""

    response = client.get(f"/v{API_VERSION}/panelists/scores/grouped-ordered-pair/slug/{panelist_slug}")
    scores = response.json()

    assert response.status_code == 200
    assert "scores" in scores
