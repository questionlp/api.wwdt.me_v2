# Copyright (c) 2018-2026 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing main routes."""

from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app, follow_redirects=False)


def test_default_page():
    """Test / route."""
    get_response = client.get("/")

    assert get_response.status_code == 200
    assert "Stats API Landing Page" in get_response.text
    assert "API v2.0 Documentation" in get_response.text
    assert "Copyright &" in get_response.text

    head_response = client.head("/")

    assert head_response.status_code == 200


def test_favicon():
    """Test /favicon.ico redirect route."""
    get_response = client.get("/favicon.ico")

    assert get_response.status_code in (301, 302)
    assert get_response.has_redirect_location

    head_response = client.head("/favicon.ico")

    assert head_response.status_code in (301, 302)
    assert head_response.has_redirect_location


def test_robots_txt():
    """Test /robots.txt route."""
    get_response = client.get("/robots.txt")

    assert get_response.status_code == 200
    assert "user-agent" in get_response.text.lower()

    head_response = client.head("/robots.txt")

    assert head_response.status_code == 200


def test_redoc_redirect_docs():
    """Test /docs redirect route."""
    get_response = client.get("/docs")

    assert get_response.status_code in (301, 302)
    assert get_response.has_redirect_location

    head_response = client.head("/docs")

    assert head_response.status_code in (301, 302)
    assert head_response.has_redirect_location


def test_redoc_redirect_redoc():
    """Test /redoc redirect route."""
    get_response = client.get("/redoc")

    assert get_response.status_code in (301, 302)
    assert get_response.has_redirect_location

    head_response = client.head("/redoc")

    assert head_response.status_code in (301, 302)
    assert head_response.has_redirect_location


def test_redoc_redirect_sub():
    """Test /v2.0/redoc redirect route."""
    get_response = client.get(f"/v{API_VERSION}/redoc")

    assert get_response.status_code in (301, 302)
    assert get_response.has_redirect_location

    head_response = client.head(f"/v{API_VERSION}/redoc")

    assert head_response.status_code in (301, 302)
    assert head_response.has_redirect_location


def test_api_v1_redirect():
    """Test /v1.0 redirect route."""
    get_response = client.get("/v1.0")

    assert get_response.status_code in (301, 302)
    assert get_response.has_redirect_location

    head_response = client.head("/v1.0")

    assert head_response.status_code in (301, 302)
    assert head_response.has_redirect_location


def test_api_v1_docs_redirect():
    """Test /v1.0/docs redirect route."""
    get_response = client.get("/v1.0/docs")

    assert get_response.status_code in (301, 302)
    assert get_response.has_redirect_location

    head_response = client.head("/v1.0/docs")

    assert head_response.status_code in (301, 302)
    assert head_response.has_redirect_location
