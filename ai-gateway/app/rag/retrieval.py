from __future__ import annotations

from .embeddings import Embeddings
from .models import (
    RetrievalRequest,
    RetrievalResult,
)
from .vector_store import VectorStore


class RetrievalEngine:
    """
    Production-ready retrieval engine.

    Responsibilities:
        - Embed query
        - Perform vector similarity search
        - Apply metadata filters
        - Return Top-K results

    Future extensions:
        - Hybrid Search (BM25 + Vector)
        - MMR Retrieval
        - Multi-query Retrieval
        - Contextual Compression
        - Cross-Encoder Re-ranking
    """

    def __init__(
        self,
        embeddings: Embeddings,
        vector_store: VectorStore,
    ):

        self.embeddings = embeddings
        self.vector_store = vector_store

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def retrieve(
        self,
        request: RetrievalRequest,
    ) -> list[RetrievalResult]:

        query_embedding = self.embeddings.embed_query(
            request.query
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=max(
                request.top_k * 3,
                request.top_k,
            ),
        )

        if request.filters:

            results = self._apply_filters(
                results,
                request.filters,
            )

        results = results[: request.top_k]

        self._statistics["queries"] = (
            self._statistics.get("queries", 0) + 1
        )

        self._statistics["returned"] = (
            self._statistics.get("returned", 0)
            + len(results)
        )

        return results

    # ---------------------------------------------------------
    # Metadata Filtering
    # ---------------------------------------------------------

    def _apply_filters(
        self,
        results: list[RetrievalResult],
        filters: dict,
    ) -> list[RetrievalResult]:

        filtered: list[RetrievalResult] = []

        for result in results:

            metadata = result.chunk.metadata.model_dump()

            matched = True

            for key, value in filters.items():

                if metadata.get(key) != value:
                    matched = False
                    break

            if matched:
                filtered.append(result)

        return filtered

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def best(
        self,
        query: str,
    ) -> RetrievalResult | None:

        results = self.retrieve(
            RetrievalRequest(
                query=query,
                top_k=1,
            )
        )

        return results[0] if results else None

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> dict:

        return dict(self._statistics)

    def clear_statistics(self):

        self._statistics.clear()

    def reset(self):

        self.clear_statistics()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self) -> dict:

        return {
            "embedding_provider": self.embeddings.provider.value,
            "vector_store": self.vector_store.store.value,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return len(self.vector_store)

    def __iter__(self):

        yield from self.configuration().items()