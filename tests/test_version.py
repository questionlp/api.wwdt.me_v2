# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Testing /v2.0/version route
"""
from fastapi.testclient import TestClient

from app.main import app
from app.config import API_VERSION

client = TestClient(app)


def test_routers_version():
    """Test /version route"""

    response = client.get(f"/v{API_VERSION}/version")
    version = response.json()

    assert response.status_code == 200
    assert "api" in version
    assert "app" in version
    assert "wwdtm" in version
