# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""App Version Models"""

from pydantic import BaseModel, Field


# region App Version Models
class Version(BaseModel):
    """Wait Wait Stats API and Application Version Information"""

    api: str = Field(title="Wait Wait Stats API Version")
    app: str = Field(title="Application Version")
    wwdtm: str = Field(title="wwdtm Version")


# endregion
