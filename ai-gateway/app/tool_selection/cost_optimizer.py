from __future__ import annotations

from collections import Counter
from typing import List, Optional

from app.tool_selection.models import (
    ToolCandidate,
)


class CostOptimizer:
    """
    Enterprise Cost Optimizer

    Responsibilities
    ----------------
    • Budget-aware tool filtering
    • Cost optimization
    • Provider preference
    • Latency-aware filtering
    • Cost statistics
    """

    def __init__(
        self,
        maximum_cost: float = float("inf"),
        preferred_provider: Optional[str] = None,
        maximum_latency_ms: Optional[float] = None,
    ):

        self._maximum_cost = maximum_cost

        self._preferred_provider = preferred_provider

        self._maximum_latency = maximum_latency_ms

        self._statistics = Counter()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    @property
    def maximum_cost(self) -> float:

        return self._maximum_cost

    @maximum_cost.setter
    def maximum_cost(
        self,
        value: float,
    ):

        self._maximum_cost = max(
            0.0,
            value,
        )

    @property
    def preferred_provider(
        self,
    ) -> Optional[str]:

        return self._preferred_provider

    @preferred_provider.setter
    def preferred_provider(
        self,
        provider: Optional[str],
    ):

        self._preferred_provider = provider

    @property
    def maximum_latency(
        self,
    ) -> Optional[float]:

        return self._maximum_latency

    @maximum_latency.setter
    def maximum_latency(
        self,
        value: Optional[float],
    ):

        self._maximum_latency = value

    # -------------------------------------------------
    # Cost Filter
    # -------------------------------------------------

    def filter_by_cost(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        filtered = [

            candidate

            for candidate

            in candidates

            if candidate.tool.average_cost
            <= self._maximum_cost

        ]

        self._statistics["cost_filtered"] += (

            len(candidates)
            - len(filtered)

        )

        return filtered

    # -------------------------------------------------
    # Latency Filter
    # -------------------------------------------------

    def filter_by_latency(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        if self._maximum_latency is None:

            return list(candidates)

        filtered = [

            candidate

            for candidate

            in candidates

            if candidate.tool.average_latency_ms
            <= self._maximum_latency

        ]

        self._statistics["latency_filtered"] += (

            len(candidates)
            - len(filtered)

        )

        return filtered

    # -------------------------------------------------
    # Provider Preference
    # -------------------------------------------------

    def prioritize_provider(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        if self._preferred_provider is None:

            return list(candidates)

        preferred = []

        others = []

        for candidate in candidates:

            if (

                candidate.tool.provider.lower()

                ==

                self._preferred_provider.lower()

            ):

                preferred.append(candidate)

            else:

                others.append(candidate)

        return preferred + others

    # -------------------------------------------------
    # Optimize
    # -------------------------------------------------

    def optimize(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        self._statistics["requests"] += 1

        optimized = self.filter_by_cost(
            candidates
        )

        optimized = self.filter_by_latency(
            optimized
        )

        optimized = self.prioritize_provider(
            optimized
        )

        optimized.sort(

            key=lambda c: (

                c.total_score,

                -c.tool.average_cost,

            ),

            reverse=True,

        )

        if optimized:

            self._statistics["successful"] += 1

        return optimized

    # -------------------------------------------------
    # Cheapest
    # -------------------------------------------------

    def cheapest(
        self,
        candidates: List[ToolCandidate],
    ) -> Optional[ToolCandidate]:

        optimized = self.optimize(
            candidates
        )

        if not optimized:

            return None

        return min(

            optimized,

            key=lambda c: (

                c.tool.average_cost,

                c.tool.average_latency_ms,

            ),

        )

    # -------------------------------------------------
    # Lowest Latency
    # -------------------------------------------------

    def fastest(
        self,
        candidates: List[ToolCandidate],
    ) -> Optional[ToolCandidate]:

        optimized = self.optimize(
            candidates
        )

        if not optimized:

            return None

        return min(

            optimized,

            key=lambda c: (

                c.tool.average_latency_ms,

                c.tool.average_cost,

            ),

        )

    # -------------------------------------------------
    # Best Value
    # -------------------------------------------------

    def best_value(
        self,
        candidates: List[ToolCandidate],
    ) -> Optional[ToolCandidate]:

        optimized = self.optimize(
            candidates
        )

        if not optimized:

            return None

        return optimized[0]

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
    # Reset
    # -------------------------------------------------

    def reset(
        self,
    ):

        self._maximum_cost = float("inf")

        self._preferred_provider = None

        self._maximum_latency = None

        self.clear_statistics()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "maximum_cost": self._maximum_cost,

            "preferred_provider": self._preferred_provider,

            "maximum_latency_ms": self._maximum_latency,

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return 3

    def __iter__(
        self,
    ):

        return iter(

            self.configuration().items()

        )