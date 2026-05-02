# Copyright (c) 2018-2026 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""App Version Models."""

from pydantic import BaseModel, Field


class Version(BaseModel):
    """Wait Wait Stats API and Application Version Information."""

    api: str = Field(title="Wait Wait Stats API Version")
    app: str = Field(title="Application Version")
    database: str | None = Field(title="Wait Wait Stats Database Version")
    wwdtm: str = Field(title="wwdtm Version")
