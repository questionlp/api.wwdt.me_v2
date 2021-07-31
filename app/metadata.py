# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""FastAPI Metdata for api.wwdt.me"""

api_metadata = {
    "description": ("Wait Wait Don't Tell Me Stats API provides endpoints "
                    "to query data for Not My Job Guests, Show Hosts, "
                    "Recording Locations, Panelists, Scorekeepers, and Shows."),
    "title": "Wait Wait Don't Tell Me Stats API v2.0",
}

tags_metadata = [
    {
        "name": "Guests",
        "description": "Retrieve data and details for Not My Job guests",
    },
    {
        "name": "Hosts",
        "description": "Retrieve data and details for hosts",
    },
    {
        "name": "Locations",
        "description": "Retrieve data and details for show recording locations",
    },
    {
        "name": "Panelists",
        "description": "Retrieve data and details for panelists",
    },
    {
        "name": "Scorekeepers",
        "description": "Retrieve data and details for scorekeepers",
    },
    {
        "name": "Shows",
        "description": "Retrieve data and details for shows",
    },
]
