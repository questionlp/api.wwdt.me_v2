# Copyright (c) 2018-2024 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Panelists Models."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, RootModel


class Panelist(BaseModel):
    """Panelist Information."""

    id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: str | None = Field(default=None, title="Panelist Slug String")
    gender: str | None = Field(default=None, title="Panelist Gender")


class Panelists(BaseModel):
    """List of Panelists."""

    panelists: list[Panelist] = Field(title="List of Panelists")


class ScoringStatistics(BaseModel):
    """Scoring Statistics."""

    minimum: int = Field(title="Minimum Score")
    maximum: int = Field(title="Maximum Score")
    mean: float = Field(title="Mean Score")
    median: float = Field(title="Median Score")
    standard_deviation: float = Field(title="Standard Deviation")
    total: int = Field("Score Total")


class DecimalScoringStatistics(BaseModel):
    """Scoring Statistics."""

    minimum: Decimal = Field(title="Minimum Score")
    maximum: Decimal = Field(title="Maximum Score")
    mean: Decimal = Field(title="Mean Score")
    median: Decimal = Field(title="Median Score")
    standard_deviation: Decimal = Field(title="Standard Deviation")
    total: Decimal = Field("Score Total")


class RankingCounts(BaseModel):
    """Ranking Counts."""

    first: int = Field(title="Count of Ranking First")
    first_tied: int = Field(title="Count of Ranking Tied for First")
    second: int = Field(title="Count of Ranking Second")
    second_tied: int = Field(title="Count of Ranking Tied for Second")
    third: int = Field(title="Count of Ranking Third")


class RankingPercentages(BaseModel):
    """Ranking Percentages."""

    first: float = Field(title="Percentage of Ranking First")
    first_tied: float = Field(title="Percentage of Ranking Tied for First")
    second: float = Field(title="Percentage of Ranking Second")
    second_tied: float = Field(title="Percentage of Ranking Tied for Second")
    third: float = Field(title="Percentage of Ranking Third")


class PanelistRankings(BaseModel):
    """Panelist Ranking Statistics."""

    rank: RankingCounts | None = Field(default=None, title="Ranking Counts")
    percentage: RankingPercentages | None = Field(
        default=None, title="Ranking Percentages"
    )


class PanelistStatistics(BaseModel):
    """Panelist Scoring and Ranking Statistics."""

    scoring: ScoringStatistics | None = Field(default=None, title="Scoring Statistics")
    scoring_decimal: DecimalScoringStatistics | None = Field(
        default=None, title="Decimal Scoring Statistics"
    )
    ranking: PanelistRankings | None = Field(default=None, title="Ranking Percentages")


class PanelistBluffs(BaseModel):
    """Panelist Bluff the Listener Statistics."""

    chosen: int | None = Field(default=None, title="Chosen Bluff the Listener Stories")
    correct: int | None = Field(
        default=None, title="Correct Bluff the Listener Stories"
    )


class MilestonesFirst(BaseModel):
    """Panelist First Appearance Milestone."""

    show_id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="First Show ID")
    show_date: str = Field(title="First Show Date")


class MilestonesMostRecent(BaseModel):
    """Panelist Most Recent Appearance Milestone."""

    show_id: Annotated[int, Field(ge=0, lt=2**31)] = Field(
        title="Most Recent Show ID"
    )
    show_date: str = Field(title="Most Recent Show Date")


class AppearanceMilestones(BaseModel):
    """Panelist Appearance Milestones."""

    first: MilestonesFirst | None = Field(default=None, title="First Appearance")
    most_recent: MilestonesMostRecent | None = Field(
        default=None, title="Most Recent Appearance"
    )


class AppearanceCounts(BaseModel):
    """Panelist Appearance Counts."""

    regular_shows: int = Field(title="Regular Show Appearances")
    all_shows: int = Field(title="All Show Appearances")
    shows_with_scores: int = Field(title="Appearances on Shows with Scores")


class ShowAppearance(BaseModel):
    """Panelist Show Appearance Information."""

    show_id: Annotated[int, Field(ge=0, lt=2**31)] = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    lightning_round_start: int | None = Field(
        default=None, title="Lightning Round Starting Score"
    )
    lightning_round_start_decimal: Decimal | None = Field(
        default=None, title="Lightning Round Starting Decimal Score"
    )
    lightning_round_correct: int | None = Field(
        default=None, title="Lightning Round Correct Answers"
    )
    lightning_round_correct_decimal: Decimal | None = Field(
        default=None, title="Lightning Round Correct Answers (Decimal)"
    )
    score: int | None = Field(default=None, title="Total Score")
    score_decimal: Decimal | None = Field(default=None, title="Total Decimal Score")
    rank: str | None = Field(default=None, title="Ranking Position")


class PanelistAppearances(BaseModel):
    """List of Panelist Show Appearances."""

    milestones: AppearanceMilestones | None = Field(
        default=None, title="Panelist Appearance Milestones"
    )
    count: AppearanceCounts | None = Field(
        default=None, title="Panelist Appearance Counts"
    )
    shows: list[ShowAppearance] | None = Field(
        default=None, title="List of Show Appearances"
    )


class PanelistDetails(Panelist):
    """Panelist Information, Statistics and Appearances."""

    statistics: PanelistStatistics | None = Field(
        default=None, title="Panelist Statistics"
    )
    bluffs: PanelistBluffs | None = Field(
        default=None, title="Panelist Bluff the Listener Statistics"
    )
    appearances: PanelistAppearances | None = Field(
        default=None, title="List of Panelist Appearances"
    )


class PanelistsDetails(BaseModel):
    """List of Panelists's Information, Statistics and Appearances."""

    panelists: list[PanelistDetails] | None = Field(
        default=None, title="List of Panelist Details"
    )


class PanelistScoresList(BaseModel):
    """List of Panelist Appearances as Show Dates and a list of corresponding Panelist scores."""

    shows: list[str] | None = Field(
        default=None, title="List of Panelist Appearances as Show Dates"
    )
    scores: list[Decimal | int] | None = Field(
        default=None, title="List of Panelist Scores"
    )


class ScoresOrderedPair(RootModel[tuple]):
    """Tuple containing a show date and the corresponding score."""

    pass


class PanelistScoresOrderedPair(BaseModel):
    """Tuple containing Panelist appearance as Show Date and score each show."""

    scores: list[ScoresOrderedPair] | None = Field(
        default=None, title="List of Ordered Pairs containing Show Date and Score"
    )


class ScoresGroupedOrderedPair(RootModel[tuple]):
    """Tuple containing a score and the occurrences of that score."""

    pass


class PanelistScoresGroupedOrderedPair(BaseModel):
    """List of tuples containing a score and the occurrences of that score."""

    scores: list[ScoresGroupedOrderedPair] | None = Field(
        default=None,
        title="List of Ordered Pairs"
        "containing scores and "
        "number of times that score "
        "has been earned",
    )
