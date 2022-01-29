# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
"""Panelists Models"""

from typing import List, Optional, Tuple
from pydantic import BaseModel, conint, Field


# region Panelist Models
class Panelist(BaseModel):
    """Panelist Information"""
    id: conint(ge=0, lt=2**31) = Field(title="Panelist ID")
    name: str = Field(title="Panelist Name")
    slug: Optional[str] = Field(default=None,
                                title="Panelist Slug String")
    gender: Optional[str] = Field(default=None,
                                  title="Panelist Gender")


class Panelists(BaseModel):
    """List of Panelists"""
    panelists: List[Panelist] = Field(title="List of Panelists")


class ScoringStatistics(BaseModel):
    """Scoring Statistics"""
    minimum: int = Field(title="Minimum Score")
    maximum: int = Field(title="Maximum Score")
    mean: float = Field(title="Mean Score")
    median: float = Field(title="Median Score")
    standard_deviation: float = Field(title="Standard Deviation")
    total: int = Field("Score Total")


class RankingCounts(BaseModel):
    """Ranking Counts"""
    first: int = Field(title="Count of Ranking First")
    first_tied: int = Field(title="Count of Ranking Tied for First")
    second: int = Field(title="Count of Ranking Second")
    second_tied: int = Field(title="Count of Ranking Tied for Second")
    third: int = Field(title="Count of Ranking Third")


class RankingPercentages(BaseModel):
    """Ranking Percentages"""
    first: float = Field(title="Percentage of Ranking First")
    first_tied: float = Field(title="Percentage of Ranking Tied for First")
    second: float = Field(title="Percentage of Ranking Second")
    second_tied: float = Field(title="Percentage of Ranking Tied for Second")
    third: float = Field(title="Percentage of Ranking Third")


class PanelistRankings(BaseModel):
    """Panelist Ranking Statistics"""
    rank: Optional[RankingCounts] = Field(default=None,
                                          title="Ranking Counts")
    percentage: Optional[RankingPercentages] = Field(default=None,
                                                     title="Ranking Percentages")


class PanelistStatistics(BaseModel):
    """Panelist Scoring and Ranking Statistics"""
    scoring: Optional[ScoringStatistics] = Field(default=None,
                                                 title="Scoring Statistics")
    ranking: Optional[PanelistRankings] = Field(default=None,
                                                title="Ranking Percentages")


class PanelistBluffs(BaseModel):
    """Panelist Bluff the Listener Statistics"""
    chosen: Optional[int] = Field(default=None,
                                  title="Chosen Bluff the Listener Stories")
    correct: Optional[int] = Field(default=None,
                                   title="Correct Bluff the Listener Stories")


class MilestonesFirst(BaseModel):
    """Panelist First Appearance Milestone"""
    show_id: conint(ge=0, lt=2**31) = Field(title="First Show ID")
    show_date: str = Field(title="First Show Date")


class MilestonesMostRecent(BaseModel):
    """Panelist Most Recent Appearance Milestone"""
    show_id: conint(ge=0, lt=2**31) = Field(title="Most Recent Show ID")
    show_date: str = Field(title="Most Recent Show Date")


class AppearanceMilestones(BaseModel):
    """Panelist Appearance Milestones"""
    first: Optional[MilestonesFirst] = Field(default=None,
                                             title="First Appearanace")
    most_recent: Optional[MilestonesMostRecent] = Field(default=None,
                                                        title="Most Recent Appearance")


class AppearanceCounts(BaseModel):
    """Panelist Appearance Counts"""
    regular_shows: int = Field(title="Regular Show Appearances")
    all_shows: int = Field(title="All Show Appearances")
    shows_with_scores: int = Field(title="Appearances on Shows with Scores")


class ShowAppearance(BaseModel):
    """Panelist Show Appearance Information"""
    show_id: conint(ge=0, lt=2**31) = Field(title="Show ID")
    date: str = Field(title="Show Date")
    best_of: bool = Field(title="Best Of Show")
    repeat_show: bool = Field(title="Repeat Show")
    lightning_round_start: Optional[int] = Field(default=None,
                                                 title="Lightning Round Starting Score")
    lightning_round_correct: Optional[int] = Field(default=None,
                                                   title="Lightning Round Correct Answers")
    score: Optional[int] = Field(default=None,
                                 title="Total Score")
    rank: Optional[str] = Field(default=None,
                                title="Ranking Position")


class PanelistAppearances(BaseModel):
    """List of Panelist Show Appearances"""
    milestones: Optional[AppearanceMilestones] = Field(default=None,
                                                       title="Panelist Appearance Milestones")
    count: Optional[AppearanceCounts] = Field(default=None,
                                              title="Panelist Appearance Counts")
    shows: Optional[List[ShowAppearance]] = Field(default=None,
                                                  title="List of Show Appearances")


class PanelistDetails(Panelist):
    """Panelist Information, Statistics and Appearances"""
    statistics: Optional[PanelistStatistics] = Field(default=None,
                                                     title="Panelist Statistics")
    bluffs: Optional[PanelistBluffs] = Field(default=None,
                                             title="Panelist Bluff the Listener Statistics")
    appearances: Optional[PanelistAppearances] = Field(default=None,
                                                       title="List of Panelist Appearances")


class PanelistsDetails(BaseModel):
    """List of Panelists's Information, Statistics and Appearances"""
    panelists: Optional[List[PanelistDetails]] = Field(default=None,
                                                       title="List of Panelist Details")


class PanelistScoresList(BaseModel):
    """Object containing a list of Panelist Appearances as Show Dates
    and a list of corresponding Panelist scores"""
    shows: Optional[List[str]] = Field(default=None,
                                       title="List of Panelist Appearances as Show Dates")
    scores: Optional[List[int]] = Field(default=None,
                                        title="List of Panelist Scores")


class ScoresOrderedPair(BaseModel):
    """Tuple containing a show date and the corresponding score"""
    __root__: Tuple = Field(title="Ordered Pair containing Show Date and Score")


class PanelistScoresOrderedPair(BaseModel):
    """Tuple containing Panelist appearance as Show Date and their
    score for that show"""
    scores: Optional[List[ScoresOrderedPair]] = Field(default=None,
                                                      title="List of Ordered Pairs containing "
                                                            "Show Date and Score")


class ScoresGroupedOrderedPair(BaseModel):
    """Tuple containing a score and their corresponding number of times
    that score had been earned"""
    __root__: Tuple = Field(title="Ordered Pair containing score and number of "
                                  "times that score had been earned")


class PanelistScoresGroupedOrderedPair(BaseModel):
    """Tuple containing scores and the corresponding number of times a
    that score had been earned"""
    scores: Optional[List[ScoresGroupedOrderedPair]] = Field(default=None,
                                                             title="List of Ordered Pairs"
                                                                   "containing scores and "
                                                                   "number of times that score "
                                                                   "has been earned")

# endregion
