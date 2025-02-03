# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Utility Methods."""

from app.utility import format_umami_analytics

_umami_disabled_config = {
    "enabled": False,
    "url": "http://test/test.js",
    "data_website_id": "test-value",
    "data_domains": "test.url",
    "data_auto_track": True,
}

_umami_enabled_config = {
    "enabled": True,
    "url": "http://test/test.js",
    "data_website_id": "test-value",
    "data_domains": "test.url",
    "data_auto_track": True,
}

_umami_invalid_config = {
    "enabled": True,
    "url": "",
    "data_website_id": "",
}


def test_format_umami_analytics_empty():
    """Test utility.format_umami_analytics with no valid configuration."""
    _analytics = format_umami_analytics(umami_analytics={})
    assert not _analytics, "Returned Umami Analytics is not None"

    _analytics = format_umami_analytics(umami_analytics=None)
    assert not _analytics, "Returned Umami Analytics is not None"


def test_format_umami_analytics_disabled():
    """Test utility.format_umami_analytics with enabled flag set to false."""
    _analytics = format_umami_analytics(umami_analytics=_umami_disabled_config)
    assert not _analytics, "Returned Umami Analytics is not None"


def test_format_umami_analytics_enabled():
    """Test utility.format_umami_analytics with enabled flag set to true."""
    _analytics = format_umami_analytics(umami_analytics=_umami_enabled_config)
    assert _analytics, "Returned Umami Analytics string is not valid"
    assert _umami_enabled_config["url"] in _analytics, (
        "Returned Umami Analytics string missing or has incorrect 'url' value"
    )
    assert _umami_enabled_config["data_website_id"] in _analytics, (
        "Returned Umami Analytics string missing or has incorrect 'website_id' value"
    )

    if _umami_enabled_config["data_auto_track"]:
        assert str(_umami_enabled_config["data_auto_track"]).lower() in _analytics, (
            "Returned Umami Analytics string missing or has missing 'data_auto_track' value"
        )

    if _umami_enabled_config["data_domains"]:
        assert _umami_enabled_config["data_domains"] in _analytics, (
            "Returned Umami Analytics string missing or has missing 'data_domains' value"
        )


def test_format_umami_analytics_invalid():
    """Test utility.format_umami_analytics with an invalid configuration."""
    _analytics = format_umami_analytics(umami_analytics=_umami_invalid_config)
    assert not _analytics, "Returned Umami Analytics is not None"
