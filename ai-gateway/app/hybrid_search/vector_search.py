from __future__ import annotations

import math
from collections import Counter
from typing import List

from app.hybrid_search.models import (
    SearchDocument,
    SearchRequest,
    SearchResult,
    SearchType,
)


class VectorSearch:
    """
    Enterprise Vector Search

    Responsibilities
    ----------------
    • Cosine similarity search
    • Embedding validation
    • Vector ranking
    • Top-K retrieval
    • Statistics collection
    """

    def __init__(
        self,
        minimum_similarity: float = 0.0,
    ):

        self._minimum_similarity = max(
            0.0,
            min(1.0, minimum_similarity),
        )

        self._statistics = Counter()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    @property
    def minimum_similarity(self) -> float:

        return self._minimum_similarity

    @minimum_similarity.setter
    def minimum_similarity(
        self,
        value: float,
    ):

        self._minimum_similarity = max(
            0.0,
            min(1.0, value),
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        request: SearchRequest,
        query_embedding: List[float],
        documents: List[SearchDocument],
    ) -> List[SearchResult]:

        self._statistics["requests"] += 1

        results = []

        for document in documents:

            if document.embedding is None:

                continue

            similarity = self.cosine_similarity(
                query_embedding,
                document.embedding,
            )

            if similarity < self._minimum_similarity:

                continue

            results.append(

                SearchResult(
                    document=document,
                    score=similarity,
                    source=SearchType.VECTOR,
                )

            )

        results.sort(
            key=lambda result: result.score,
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
    # Cosine Similarity
    # -------------------------------------------------

    def cosine_similarity(
        self,
        vector1: List[float],
        vector2: List[float],
    ) -> float:

        if len(vector1) != len(vector2):

            raise ValueError(
                "Embedding dimensions do not match."
            )

        dot_product = sum(

            a * b

            for a, b

            in zip(
                vector1,
                vector2,
            )

        )

        magnitude1 = math.sqrt(

            sum(
                value * value
                for value
                in vector1
            )

        )

        magnitude2 = math.sqrt(

            sum(
                value * value
                for value
                in vector2
            )

        )

        if magnitude1 == 0 or magnitude2 == 0:

            return 0.0

        return dot_product / (
            magnitude1 * magnitude2
        )

    # -------------------------------------------------
    # Best Match
    # -------------------------------------------------

    def best(
        self,
        request: SearchRequest,
        query_embedding: List[float],
        documents: List[SearchDocument],
    ) -> SearchResult | None:

        results = self.search(
            request,
            query_embedding,
            documents,
        )

        if not results:

            return None

        return results[0]

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

        self._minimum_similarity = 0.0

        self.clear_statistics()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "algorithm": "cosine",

            "minimum_similarity":
                self._minimum_similarity,

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