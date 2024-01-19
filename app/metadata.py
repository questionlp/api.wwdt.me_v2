# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""FastAPI Metadata for api.wwdt.me."""

from email_validator import EmailNotValidError, validate_email

from app.config import load_config

_config = load_config()
_contact_info = {}
if "settings" in _config and _config["settings"]:
    _settings = _config["settings"]
    if "contact_name" in _settings and "contact_email" in _settings:
        try:
            _name = _settings.get("contact_name")
            if not _name and not _name.strip():
                _name: str = "API Developer"

            _email = str(_settings.get("contact_email"))
            valid_email = validate_email(_email)

            _url = _settings.get("contact_url", None)
            if not _url or not str(_url).strip():
                _url = None

            _contact_info = {
                "name": _name,
                "email": str(_settings.get("contact_email")),
                "url": _url,
            }
        except EmailNotValidError:
            _contact_info = {
                "name": "API Developer",
                "email": "api@example.org",
            }

app_metadata = {
    "title": "Wait Wait Don't Tell Me Stats API",
    "description": """
Wait Wait Don't Tell Me Stats API provides endpoints to query data for Not My
Job Guests, Show Hosts, Recording Locations, Panelists, Scorekeepers, and
Shows.

Source code for this application is available on
[GitHub](https://github.com/questionlp/api.wwdt.me_v2).
    """,
    "contact_info": _contact_info,
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
}

tags_metadata = [
    {
        "name": "Guests",
        "description": "Retrieve information and appearances for Not My Job Guests",
    },
    {
        "name": "Hosts",
        "description": "Retrieve information and appearances for Hosts",
    },
    {
        "name": "Locations",
        "description": "Retrieve information and appearances for Locations",
    },
    {
        "name": "Panelists",
        "description": "Retrieve information, statistics and appearances for Panelists",
    },
    {
        "name": "Scorekeepers",
        "description": "Retrieve information and appearances for Scorekeepers",
    },
    {
        "name": "Shows",
        "description": "Retrieve information and details for Shows",
    },
    {
        "name": "Version",
        "description": "Retrieve Wait Wait Stats API and Application Version Information",
    },
]
