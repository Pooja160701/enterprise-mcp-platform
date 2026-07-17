from __future__ import annotations

from collections import Counter
from typing import List, Optional

from app.tool_selection.models import (
    SelectionResult,
    ToolCandidate,
)


class ConfidenceSelector:
    """
    Enterprise Confidence Selector

    Responsibilities
    ----------------
    • Confidence threshold validation
    • Select highest-confidence tool
    • Confidence-aware fallback
    • Candidate filtering
    • Statistics collection
    """

    def __init__(
        self,
        minimum_confidence: float = 0.70,
    ):

        self._minimum_confidence = max(
            0.0,
            min(1.0, minimum_confidence),
        )

        self._statistics = Counter()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    @property
    def minimum_confidence(
        self,
    ) -> float:

        return self._minimum_confidence

    @minimum_confidence.setter
    def minimum_confidence(
        self,
        value: float,
    ):

        self._minimum_confidence = max(
            0.0,
            min(1.0, value),
        )

    # -------------------------------------------------
    # Confidence Check
    # -------------------------------------------------

    def confident(
        self,
        candidate: ToolCandidate,
    ) -> bool:

        return (

            candidate.total_score

            >=

            self._minimum_confidence

        )

    # -------------------------------------------------
    # Filter
    # -------------------------------------------------

    def filter(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        filtered = [

            candidate

            for candidate

            in candidates

            if self.confident(candidate)

        ]

        self._statistics["requests"] += 1

        self._statistics["accepted"] += len(
            filtered
        )

        self._statistics["rejected"] += (

            len(candidates)

            -

            len(filtered)

        )

        return filtered

    # -------------------------------------------------
    # Select
    # -------------------------------------------------

    def select(
        self,
        candidates: List[ToolCandidate],
    ) -> SelectionResult:

        ranked = sorted(

            candidates,

            key=lambda c: c.total_score,

            reverse=True,

        )

        confident = self.filter(
            ranked
        )

        if confident:

            self._statistics["selected"] += 1

            return SelectionResult(

                selected=confident[0].tool,

                candidates=ranked,

                fallback_tools=[

                    candidate.tool

                    for candidate

                    in confident[1:]

                ],

                reason=(
                    f"Selected tool with confidence "
                    f"{confident[0].total_score:.3f}"
                ),

            )

        self._statistics["fallback"] += 1

        return SelectionResult(

            selected=None,

            candidates=ranked,

            fallback_tools=[

                candidate.tool

                for candidate

                in ranked

            ],

            reason=(
                "No tool met the minimum "
                "confidence threshold."
            ),

        )

    # -------------------------------------------------
    # Best Candidate
    # -------------------------------------------------

    def best(
        self,
        candidates: List[ToolCandidate],
    ) -> Optional[ToolCandidate]:

        filtered = self.filter(
            candidates
        )

        if not filtered:

            return None

        return max(

            filtered,

            key=lambda c: c.total_score,

        )

    # -------------------------------------------------
    # Fallback Candidates
    # -------------------------------------------------

    def fallbacks(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        ranked = sorted(

            candidates,

            key=lambda c: c.total_score,

            reverse=True,

        )

        filtered = self.filter(
            ranked
        )

        if len(filtered) <= 1:

            return []

        return filtered[1:]

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

        self._minimum_confidence = 0.70

        self.clear_statistics()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "minimum_confidence":
            self._minimum_confidence,

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return 1

    def __iter__(
        self,
    ):

        return iter(
            self.configuration().items()
        )