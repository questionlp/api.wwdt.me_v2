# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/version route."""

from fastapi.testclient import TestClient
from wwdtm import VERSION as WWDTM_VERSION

from app.config import API_VERSION, APP_VERSION
from app.main import app

client = TestClient(app)


def test_version():
    """Test /version route."""
    response = client.get(f"/v{API_VERSION}/version")
    version = response.json()

    assert response.status_code == 200
    assert "api" in version
    assert version["api"] == API_VERSION
    assert "app" in version
    assert version["app"] == APP_VERSION
    assert "wwdtm" in version
    assert version["wwdtm"] == WWDTM_VERSION
