from __future__ import annotations

from collections import Counter
from typing import List

from app.hybrid_search.models import (
    SearchRequest,
    SearchResult,
)


class ReRanker:
    """
    Enterprise ReRanker

    Responsibilities
    ----------------
    • Re-score retrieved documents
    • Pluggable ranking backend
    • Top-K selection
    • Statistics collection

    Future implementations:
        - CrossEncoder
        - Cohere Rerank
        - BGE Reranker
        - Azure Semantic Ranker
    """

    def __init__(
        self,
        top_k: int = 10,
    ):

        self._top_k = max(1, top_k)

        self._statistics = Counter()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    @property
    def top_k(self) -> int:

        return self._top_k

    @top_k.setter
    def top_k(
        self,
        value: int,
    ):

        self._top_k = max(1, value)

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def rerank(
        self,
        request: SearchRequest,
        results: List[SearchResult],
    ) -> List[SearchResult]:

        self._statistics["requests"] += 1

        if not results:

            return []

        query_tokens = self._tokenize(
            request.query
        )

        reranked = []

        for result in results:

            score = self.score(
                query_tokens,
                result.document.text,
            )

            result.score = score

            reranked.append(
                result
            )

        reranked.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        for rank, result in enumerate(
            reranked,
            start=1,
        ):
            result.rank = rank

        reranked = reranked[
            : min(
                request.top_k,
                self._top_k,
            )
        ]

        self._statistics["reranked"] += len(
            reranked
        )

        return reranked

    # -------------------------------------------------
    # Scoring
    # -------------------------------------------------

    def score(
        self,
        query_tokens: List[str],
        document: str,
    ) -> float:

        """
        Default lexical overlap score.

        Replace this method later with:

        CrossEncoder.predict()
        Cohere.rerank()
        Azure Semantic Ranker
        etc.
        """

        document_tokens = set(
            self._tokenize(document)
        )

        if not document_tokens:

            return 0.0

        overlap = len(
            document_tokens.intersection(
                query_tokens
            )
        )

        return overlap / len(
            document_tokens
        )

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _tokenize(
        self,
        text: str,
    ) -> List[str]:

        return [

            token

            for token

            in text.lower().split()

            if token

        ]

    # -------------------------------------------------
    # Convenience
    # -------------------------------------------------

    def best(
        self,
        request: SearchRequest,
        results: List[SearchResult],
    ) -> SearchResult | None:

        reranked = self.rerank(
            request,
            results,
        )

        if not reranked:

            return None

        return reranked[0]

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

        self._top_k = 10

        self.clear_statistics()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "algorithm": "lexical",

            "top_k": self._top_k,

            "replaceable": True,

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