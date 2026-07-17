from __future__ import annotations

from collections import Counter
from typing import List, Optional

from app.tool_selection.models import (
    RankingWeights,
    ToolCandidate,
    ToolMetadata,
)


class ToolRanker:
    """
    Enterprise Tool Ranker

    Responsibilities
    ----------------
    • Rank candidate tools
    • Weighted score calculation
    • Normalize latency and cost
    • Reliability-aware ranking
    • Statistics collection
    """

    def __init__(
        self,
        weights: Optional[RankingWeights] = None,
    ):

        self._weights = (
            weights
            if weights is not None
            else RankingWeights()
        )

        self._statistics = Counter()

    # -------------------------------------------------
    # Normalization
    # -------------------------------------------------

    @staticmethod
    def _normalize_inverse(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:

        if maximum <= minimum:

            return 1.0

        return max(
            0.0,
            min(
                1.0,
                (maximum - value)
                / (maximum - minimum),
            ),
        )

    # -------------------------------------------------
    # Score One Candidate
    # -------------------------------------------------

    def score(
        self,
        candidate: ToolCandidate,
        min_latency: float,
        max_latency: float,
        min_cost: float,
        max_cost: float,
    ) -> ToolCandidate:

        tool = candidate.tool

        candidate.latency_score = round(
            self._normalize_inverse(
                tool.average_latency_ms,
                min_latency,
                max_latency,
            ),
            3,
        )

        candidate.cost_score = round(
            self._normalize_inverse(
                tool.average_cost,
                min_cost,
                max_cost,
            ),
            3,
        )

        candidate.reliability_score = round(
            tool.reliability,
            3,
        )

        candidate.confidence_score = round(
            tool.confidence,
            3,
        )

        total = (

            self._weights.capability
            * candidate.capability_score

            +

            self._weights.confidence
            * candidate.confidence_score

            +

            self._weights.reliability
            * candidate.reliability_score

            +

            self._weights.latency
            * candidate.latency_score

            +

            self._weights.cost
            * candidate.cost_score

        )

        candidate.total_score = round(
            total,
            3,
        )

        self._statistics["scored"] += 1

        return candidate

    # -------------------------------------------------
    # Rank Candidates
    # -------------------------------------------------

    def rank(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        if not candidates:

            return []

        latencies = [
            c.tool.average_latency_ms
            for c in candidates
        ]

        costs = [
            c.tool.average_cost
            for c in candidates
        ]

        min_latency = min(latencies)
        max_latency = max(latencies)

        min_cost = min(costs)
        max_cost = max(costs)

        ranked = [

            self.score(
                candidate,
                min_latency,
                max_latency,
                min_cost,
                max_cost,
            )

            for candidate

            in candidates

        ]

        ranked.sort(

            key=lambda c: c.total_score,

            reverse=True,

        )

        self._statistics["requests"] += 1

        return ranked

    # -------------------------------------------------
    # Best Candidate
    # -------------------------------------------------

    def best(
        self,
        candidates: List[ToolCandidate],
    ) -> Optional[ToolCandidate]:

        ranked = self.rank(
            candidates
        )

        if not ranked:

            return None

        return ranked[0]

    # -------------------------------------------------
    # Top N
    # -------------------------------------------------

    def top(
        self,
        candidates: List[ToolCandidate],
        limit: int = 5,
    ) -> List[ToolCandidate]:

        return self.rank(
            candidates
        )[:limit]

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    @property
    def weights(
        self,
    ) -> RankingWeights:

        return self._weights

    def set_weights(
        self,
        weights: RankingWeights,
    ):

        self._weights = weights

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ) -> dict:

        return dict(
            self._statistics
        )

    def clear_statistics(
        self,
    ):

        self._statistics.clear()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def reset(self):

        self._weights = RankingWeights()

        self.clear_statistics()

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(self):

        return 5

    def __iter__(self):

        return iter(

            [

                (
                    "capability",
                    self._weights.capability,
                ),
                (
                    "confidence",
                    self._weights.confidence,
                ),
                (
                    "reliability",
                    self._weights.reliability,
                ),
                (
                    "latency",
                    self._weights.latency,
                ),
                (
                    "cost",
                    self._weights.cost,
                ),

            ]

        )