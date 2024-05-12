# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Pronouns Models."""

from typing import Annotated

from pydantic import BaseModel, Field


class Pronouns(BaseModel):
    """Pronouns Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Pronouns ID")
    pronouns: str = Field(title="Pronouns")


class PronounsInfoList(BaseModel):
    """List containing Pronouns Information."""

    pronouns: list[Pronouns] = Field(title="List of Pronouns")
