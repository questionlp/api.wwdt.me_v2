# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""Application Configuration"""

import os
from typing import Any, Dict

from dotenv import find_dotenv, load_dotenv

API_VERSION="2.0"
APP_VERSION="1.0.0a1"

def load_config() -> Dict[str, Any]:
    load_dotenv(find_dotenv())
    return {
        "host": os.getenv("DATABASE_HOST"),
        "user": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
        "database": os.getenv("DATABASE_NAME"),
        "port": os.getenv("DATABASE_PORT", 3306),
        "raise_on_warnings": bool(os.getenv("DATABASE_RAISE_ON_WARNINGS", True)),
        "compress": bool(os.getenv("DATABASE_COMPRESSION", True)),
        "charset": os.getenv("DATABASE_CHARSET", "utf8mb4"),
        "collation": os.getenv("DATABASE_COLLATION", "utf8mb4_unicode_ci"),
    }

