from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

from app.hybrid_search.models import SearchDocument


class MetadataFilter:
    """
    Enterprise Metadata Filter

    Responsibilities
    ----------------
    • Exact metadata matching
    • Numeric comparison
    • Range filtering
    • List membership
    • Multiple filter conditions
    """

    def __init__(self):

        self._statistics = Counter()

    # -------------------------------------------------
    # Filter
    # -------------------------------------------------

    def filter(
        self,
        documents: List[SearchDocument],
        filters: Dict[str, Any],
    ) -> List[SearchDocument]:

        self._statistics["requests"] += 1

        if not filters:

            return list(documents)

        results = []

        for document in documents:

            if self.matches(
                document.metadata,
                filters,
            ):
                results.append(document)

        self._statistics["matched"] += len(
            results
        )

        self._statistics["filtered"] += (
            len(documents)
            - len(results)
        )

        return results

    # -------------------------------------------------
    # Match
    # -------------------------------------------------

    def matches(
        self,
        metadata: Dict[str, Any],
        filters: Dict[str, Any],
    ) -> bool:

        for key, expected in filters.items():

            if key not in metadata:

                return False

            value = metadata[key]

            if isinstance(expected, dict):

                if not self._compare(
                    value,
                    expected,
                ):
                    return False

            elif isinstance(expected, list):

                if isinstance(value, list):

                    if not any(
                        item in value
                        for item in expected
                    ):
                        return False

                else:

                    if value not in expected:
                        return False

            else:

                if value != expected:
                    return False

        return True

    # -------------------------------------------------
    # Comparison Operators
    # -------------------------------------------------

    def _compare(
        self,
        value: Any,
        condition: Dict[str, Any],
    ) -> bool:

        for operator, expected in condition.items():

            if operator == "$gt":

                if not value > expected:
                    return False

            elif operator == "$gte":

                if not value >= expected:
                    return False

            elif operator == "$lt":

                if not value < expected:
                    return False

            elif operator == "$lte":

                if not value <= expected:
                    return False

            elif operator == "$eq":

                if not value == expected:
                    return False

            elif operator == "$ne":

                if not value != expected:
                    return False

            elif operator == "$in":

                if value not in expected:
                    return False

            elif operator == "$nin":

                if value in expected:
                    return False

            else:

                raise ValueError(
                    f"Unsupported operator: {operator}"
                )

        return True

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

        self.clear_statistics()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "supported_operators": [

                "$eq",
                "$ne",
                "$gt",
                "$gte",
                "$lt",
                "$lte",
                "$in",
                "$nin",

            ]

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return len(
            self.configuration()[
                "supported_operators"
            ]
        )

    def __iter__(
        self,
    ):

        return iter(
            self.configuration().items()
        )