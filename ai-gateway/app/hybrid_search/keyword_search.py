from __future__ import annotations

from collections import Counter
from typing import List

from app.hybrid_search.models import (
    SearchDocument,
    SearchRequest,
    SearchResult,
    SearchType,
)


class KeywordSearch:
    """
    Enterprise Keyword Search

    Responsibilities
    ----------------
    • Exact keyword matching
    • Case-insensitive search
    • Simple relevance scoring
    • Ranking
    • Statistics collection
    """

    def __init__(self):

        self._statistics = Counter()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        request: SearchRequest,
        documents: List[SearchDocument],
    ) -> List[SearchResult]:

        self._statistics["requests"] += 1

        query_terms = self._tokenize(
            request.query
        )

        results = []

        for document in documents:

            score = self._score(
                query_terms,
                document.text,
            )

            if score == 0:
                continue

            results.append(

                SearchResult(
                    document=document,
                    score=score,
                    source=SearchType.KEYWORD,
                )

            )

        results.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):
            result.rank = rank

        self._statistics["matched"] += len(
            results
        )

        return results[: request.top_k]

    # -------------------------------------------------
    # Score
    # -------------------------------------------------

    def _score(
        self,
        query_terms: List[str],
        text: str,
    ) -> float:

        tokens = self._tokenize(text)

        if not tokens:
            return 0.0

        count = sum(

            tokens.count(term)

            for term

            in query_terms

        )

        return float(count)

    # -------------------------------------------------
    # Tokenization
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
            "algorithm": "keyword",
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