# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/hosts routes."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_hosts():
    """Test /v2.0/hosts route."""
    response = client.get(f"/v{API_VERSION}/hosts")
    hosts = response.json()

    assert response.status_code == 200
    assert "hosts" in hosts
    assert "id" in hosts["hosts"][0]
    assert "name" in hosts["hosts"][0]
    assert "pronouns" in hosts["hosts"][0]
    assert "slug" in hosts["hosts"][0]


@pytest.mark.parametrize("host_id", [2])
def test_hosts_id(host_id: int):
    """Test /v2.0/hosts/id/{host_id} route."""
    response = client.get(f"/v{API_VERSION}/hosts/id/{host_id}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert host["id"] == host_id
    assert "name" in host
    assert "pronouns" in host
    assert "slug" in host


@pytest.mark.parametrize("host_slug", ["luke-burbank"])
def test_hosts_slug(host_slug: str):
    """Test /v2.0/hosts/slug/{host_slug} route."""
    response = client.get(f"/v{API_VERSION}/hosts/slug/{host_slug}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert "name" in host
    assert "pronouns" in host
    assert "slug" in host
    assert host["slug"] == host_slug


def test_hosts_details():
    """Test /v2.0/hosts/details route."""
    response = client.get(f"/v{API_VERSION}/hosts/details")
    hosts = response.json()

    assert response.status_code == 200
    assert "hosts" in hosts
    assert "id" in hosts["hosts"][0]
    assert "name" in hosts["hosts"][0]
    assert "pronouns" in hosts["hosts"][0]
    assert "slug" in hosts["hosts"][0]
    assert "appearances" in hosts["hosts"][0]


@pytest.mark.parametrize("host_id", [2])
def test_hosts_details_id(host_id: int):
    """Test /v2.0/hosts/details/id/{host_id} route."""
    response = client.get(f"/v{API_VERSION}/hosts/details/id/{host_id}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert host["id"] == host_id
    assert "name" in host
    assert "pronouns" in host
    assert "slug" in host
    assert "appearances" in host


@pytest.mark.parametrize("host_slug", ["luke-burbank"])
def test_hosts_details_slug(host_slug: str):
    """Test /v2.0/hosts/details/slug/{host_slug} route."""
    response = client.get(f"/v{API_VERSION}/hosts/details/slug/{host_slug}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert "name" in host
    assert "pronouns" in host
    assert "slug" in host
    assert host["slug"] == host_slug
    assert "appearances" in host


def test_hosts_random():
    """Test /v2.0/hosts/random route."""
    response = client.get(f"/v{API_VERSION}/hosts/random")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert "name" in host
    assert "pronouns" in host
    assert "slug" in host


def test_hosts_random_details():
    """Test /v2.0/hosts/details/random route."""
    response = client.get(f"/v{API_VERSION}/hosts/details/random")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert "name" in host
    assert "pronouns" in host
    assert "slug" in host
    assert "appearances" in host


def test_hosts_random_id():
    """Test /v2.0/hosts/random/id route."""
    response = client.get(f"/v{API_VERSION}/hosts/random/id")
    _id = response.json()

    assert response.status_code == 200
    assert "id" in _id
    assert isinstance(_id["id"], int)


def test_hosts_random_slug():
    """Test /v2.0/hosts/random/slug route."""
    response = client.get(f"/v{API_VERSION}/hosts/random/slug")
    _slug = response.json()

    assert response.status_code == 200
    assert "slug" in _slug
    assert isinstance(_slug["slug"], str)
