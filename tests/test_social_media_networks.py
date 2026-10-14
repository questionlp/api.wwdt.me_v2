# Copyright (c) 2018-2026 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/social-media-networks routes."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_get_social_media_networks():
    """Test /v2.0/social-media-networks route."""
    response = client.get(f"/v{API_VERSION}/social-media-networks")
    networks = response.json()

    assert response.status_code == 200
    assert "networks" in networks
    assert "id" in networks["networks"][0]
    assert "network" in networks["networks"][0]
    assert "slug" in networks["networks"][0]


@pytest.mark.parametrize("social_media_network_id", [1])
def test_get_social_media_network_by_id(social_media_network_id: int):
    """Test /v2.0/social-media-networks/id/{social_media_network_id} route."""
    response = client.get(
        f"/v{API_VERSION}/social-media-networks/id/{social_media_network_id}"
    )
    network_info = response.json()

    assert response.status_code == 200
    assert "id" in network_info
    assert network_info["id"] == social_media_network_id
    assert "network" in network_info
    assert "slug" in network_info


@pytest.mark.parametrize("social_media_network_id", [0])
def test_get_social_media_network_by_id_not_found(social_media_network_id: int):
    """Test /v2.0/social-media-networks/id/{social_media_network_id} route."""
    response = client.get(
        f"/v{API_VERSION}/social-media-networks/id/{social_media_network_id}"
    )
    network_info = response.json()

    assert response.status_code == 404
    assert "slug" not in network_info


@pytest.mark.parametrize("social_media_network_slug", ["bluesky"])
def test_get_social_media_network_by_slug(social_media_network_slug: str):
    """Test /v2.0/social-media-networks/id/{social_media_network_id} route."""
    response = client.get(
        f"/v{API_VERSION}/social-media-networks/slug/{social_media_network_slug}"
    )
    network_info = response.json()

    assert response.status_code == 200
    assert "slug" in network_info
    assert network_info["slug"] == social_media_network_slug
    assert "network" in network_info
    assert "id" in network_info


@pytest.mark.parametrize("social_media_network_slug", ["non-existent-network"])
def test_get_social_media_network_by_slug_not_found(social_media_network_slug: str):
    """Test /v2.0/social-media-networks/id/{social_media_network_slug} route."""
    response = client.get(
        f"/v{API_VERSION}/social-media-networks/slug/{social_media_network_slug}"
    )
    network_info = response.json()

    assert response.status_code == 404
    assert "slug" not in network_info
