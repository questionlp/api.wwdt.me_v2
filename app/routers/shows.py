# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""API routes for Scorekeeper endpoints"""

from app.config import API_VERSION, load_database_config
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
from pydantic import constr, PositiveInt
from wwdtm.show import details, info

router = APIRouter(
    prefix=f"/v{API_VERSION}/shows"
)
_database_config = load_database_config()
_database_connection = mysql.connector.connect(**_database_config)
_database_connection.autocommit = True

#region Routes



#endregion
