from __future__ import annotations

from collections import Counter
from typing import Dict, List

from app.hybrid_search.models import SearchResult


class RankingFusion:
    """
    Enterprise Reciprocal Rank Fusion (RRF)

    Responsibilities
    ----------------
    • Reciprocal Rank Fusion
    • Merge multiple ranked lists
    • Stable ranking
    • Statistics collection
    """

    def __init__(
        self,
        k: int = 60,
    ):

        self._k = max(1, k)

        self._statistics = Counter()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    @property
    def k(self) -> int:

        return self._k

    @k.setter
    def k(
        self,
        value: int,
    ):

        self._k = max(1, value)

    # -------------------------------------------------
    # Fusion
    # -------------------------------------------------

    def fuse(
        self,
        result_sets: List[List[SearchResult]],
        top_k: int | None = None,
    ) -> List[SearchResult]:

        self._statistics["requests"] += 1

        if not result_sets:

            return []

        fused_scores: Dict[str, float] = {}

        representative: Dict[str, SearchResult] = {}

        for results in result_sets:

            for rank, result in enumerate(
                results,
                start=1,
            ):

                document_id = result.document.id

                representative.setdefault(
                    document_id,
                    result,
                )

                fused_scores[
                    document_id
                ] = fused_scores.get(
                    document_id,
                    0.0,
                ) + self._rrf_score(rank)

        fused_results = []

        for document_id, score in fused_scores.items():

            result = representative[
                document_id
            ]

            result.score = score

            fused_results.append(
                result
            )

        fused_results.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        for rank, result in enumerate(
            fused_results,
            start=1,
        ):

            result.rank = rank

        self._statistics["merged_documents"] += len(
            fused_results
        )

        if top_k is not None:

            fused_results = fused_results[:top_k]

        return fused_results

    # -------------------------------------------------
    # RRF
    # -------------------------------------------------

    def _rrf_score(
        self,
        rank: int,
    ) -> float:

        return 1.0 / (
            self._k + rank
        )

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

        self._k = 60

        self.clear_statistics()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "algorithm":
                "Reciprocal Rank Fusion",

            "k":
                self._k,

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return 2

    def __iter__(
        self,
    ):

        return iter(
            self.configuration().items()
        )