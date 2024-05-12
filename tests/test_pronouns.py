# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/pronouns routes."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_pronouns():
    """Test /v2.0/pronouns route."""
    response = client.get(f"/v{API_VERSION}/pronouns")
    pronouns = response.json()

    assert response.status_code == 200
    assert "pronouns" in pronouns
    assert "id" in pronouns["pronouns"][0]
    assert "pronouns" in pronouns["pronouns"][0]


@pytest.mark.parametrize("pronouns_id", [1])
def test_pronouns_id(pronouns_id: int):
    """Test /v2.0/pronouns/id/{pronouns_id} route."""
    response = client.get(f"/v{API_VERSION}/pronouns/id/{pronouns_id}")
    pronouns_info = response.json()

    assert response.status_code == 200
    assert "id" in pronouns_info
    assert pronouns_info["id"] == pronouns_id
    assert "pronouns" in pronouns_info
