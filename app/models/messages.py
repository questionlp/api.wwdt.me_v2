# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Response Message Models."""

from pydantic import BaseModel, Field


class MessageDetails(BaseModel):
    """Response Message Details."""

    detail: str = Field(title="Message details")
