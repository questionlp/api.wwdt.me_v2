# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Testing /v2.0/hosts routes
"""
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.config import API_VERSION

client = TestClient(app)


def test_hosts():
    """Test /v2.0/hosts route"""

    response = client.get(f"/v{API_VERSION}/hosts")
    hosts = response.json()

    assert response.status_code == 200
    assert "hosts" in hosts
    assert "id" in hosts["hosts"][0]
    assert "name" in hosts["hosts"][0]
    assert "slug" in hosts["hosts"][0]


@pytest.mark.parametrize("host_id", [2])
def test_hosts_id(host_id: int):
    """Test /v2.0/hosts/id/{host_id} route"""

    response = client.get(f"/v{API_VERSION}/hosts/id/{host_id}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert host["id"] == host_id
    assert "name" in host
    assert "slug" in host


@pytest.mark.parametrize("host_slug", ["luke-burbank"])
def test_hosts_slug(host_slug: str):
    """Test /v2.0/hosts/slug/{host_slug} route"""

    response = client.get(f"/v{API_VERSION}/hosts/slug/{host_slug}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert "name" in host
    assert "slug" in host
    assert host["slug"] == host_slug


def test_hosts_details():
    """Test /v2.0/hosts/details route"""

    response = client.get(f"/v{API_VERSION}/hosts/details")
    hosts = response.json()

    assert response.status_code == 200
    assert "hosts" in hosts
    assert "id" in hosts["hosts"][0]
    assert "name" in hosts["hosts"][0]
    assert "slug" in hosts["hosts"][0]
    assert "appearances" in hosts["hosts"][0]


@pytest.mark.parametrize("host_id", [2])
def test_hosts_details_id(host_id: int):
    """Test /v2.0/hosts/details/id/{host_id} route"""

    response = client.get(f"/v{API_VERSION}/hosts/details/id/{host_id}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert host["id"] == host_id
    assert "name" in host
    assert "slug" in host
    assert "appearances" in host


@pytest.mark.parametrize("host_slug", ["luke-burbank"])
def test_hosts_details_slug(host_slug: str):
    """Test /v2.0/hosts/details/slug/{host_slug} route"""

    response = client.get(f"/v{API_VERSION}/hosts/details/slug/{host_slug}")
    host = response.json()

    assert response.status_code == 200
    assert "id" in host
    assert "name" in host
    assert "slug" in host
    assert host["slug"] == host_slug
    assert "appearances" in host
