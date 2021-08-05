# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI Metdata for api.wwdt.me"""

from typing import Dict, List

app_metadata = {
    "title": "Wait Wait Don't Tell Me Stats API",
    "description": """
Wait Wait Don't Tell Me Stats API provides endpoints to query data for Not My
Job Guests, Show Hosts, Recording Locations, Panelists, Scorekeepers, and
Shows.

Source code for this application is available on
[GitHub](https://github.com/questionlp/api.wwdt.me_fastapi).
    """,
    "contact_info": {
        "name": "Linh Pham",
        "email": "dev@wwdt.me",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
}

tags_metadata: List[Dict[str, str]] = [
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
