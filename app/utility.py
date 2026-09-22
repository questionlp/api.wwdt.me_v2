# Copyright (c) 2018-2026 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Utility functions used by api.wwdt.me."""

from datetime import datetime

import pytz

_utc_timezone = pytz.timezone("UTC")


def current_year(time_zone: pytz.timezone = _utc_timezone):
    """Return the current year."""
    now = datetime.now(time_zone)
    return now.strftime("%Y")


def format_umami_analytics(umami_analytics: dict = None) -> str:
    """Return formatted string for Umami Analytics."""
    if not umami_analytics:
        return None

    _enabled = bool(umami_analytics.get("enabled", False))

    if not _enabled:
        return None

    url = umami_analytics.get("url")
    website_id = umami_analytics.get("data_website_id")
    auto_track = bool(umami_analytics.get("data_auto_track", True))
    host_url = umami_analytics.get("data_host_url")
    domains = umami_analytics.get("data_domains")

    if url and website_id:
        host_url_prop = f'data-host-url="{host_url}"' if host_url else ""
        auto_track_prop = f'data-auto-track="{str(auto_track).lower()}"'
        domains_prop = f'data-domains="{domains}"' if domains else ""

        props = " ".join([host_url_prop, auto_track_prop, domains_prop])
        return f'<script defer src="{url}" data-website-id="{website_id}" {props.strip()}></script>'

    return None


def time_zone_parser(time_zone: str) -> pytz.timezone:
    """Parses a time zone name into a pytz.timezone object.

    Returns pytz.timezone object and string if time_zone is valid.
    Otherwise, returns UTC if time zone is not a valid tz value.
    """
    try:
        time_zone_object = pytz.timezone(time_zone)
        time_zone_string = time_zone_object.zone
    except (pytz.UnknownTimeZoneError, AttributeError, ValueError):
        time_zone_object = pytz.timezone("UTC")
        time_zone_string = time_zone_object.zone

    return time_zone_object, time_zone_string
