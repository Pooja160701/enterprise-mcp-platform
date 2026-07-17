from __future__ import annotations

from .embeddings import Embeddings
from .models import (
    DocumentChunk,
    RetrievalResult,
    VectorStoreStats,
    VectorStoreType,
)


class VectorStore:
    """
    Production-ready in-memory vector store.

    Current implementation:
        - In-memory vector storage

    Future implementations:
        - ChromaDB
        - FAISS
        - Pinecone
        - Qdrant
        - Milvus

    Public API remains unchanged.
    """

    def __init__(
        self,
        embeddings: Embeddings,
        store: VectorStoreType = VectorStoreType.MEMORY,
    ):

        self.embeddings = embeddings
        self.store = store

        self._chunks: dict[str, DocumentChunk] = {}

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def add(
        self,
        chunks: list[DocumentChunk],
    ):

        for chunk in chunks:

            if not chunk.embedding:

                chunk.embedding = self.embeddings.embed_query(
                    chunk.text
                )

            self._chunks[chunk.id] = chunk

        self._statistics["added"] = (
            self._statistics.get("added", 0)
            + len(chunks)
        )

    def delete(
        self,
        chunk_id: str,
    ):

        if chunk_id in self._chunks:

            del self._chunks[chunk_id]

            self._statistics["deleted"] = (
                self._statistics.get("deleted", 0)
                + 1
            )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[RetrievalResult]:

        results: list[RetrievalResult] = []

        for chunk in self._chunks.values():

            score = self.embeddings.cosine_similarity(
                query_embedding,
                chunk.embedding,
            )

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    score=score,
                )
            )

        results.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        self._statistics["searches"] = (
            self._statistics.get("searches", 0)
            + 1
        )

        self._statistics["returned"] = (
            self._statistics.get("returned", 0)
            + min(top_k, len(results))
        )

        return results[:top_k]

    def get(
        self,
        chunk_id: str,
    ) -> DocumentChunk | None:

        return self._chunks.get(chunk_id)

    def clear(self):

        self._chunks.clear()

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> VectorStoreStats:

        dimensions = 0

        if self._chunks:

            dimensions = len(
                next(iter(self._chunks.values())).embedding
            )

        return VectorStoreStats(
            documents=len(
                {
                    c.document_id
                    for c in self._chunks.values()
                }
            ),
            chunks=len(self._chunks),
            dimensions=dimensions,
            provider=self.embeddings.provider,
            store=self.store,
        )

    def runtime_statistics(self) -> dict:

        return dict(self._statistics)

    def clear_statistics(self):

        self._statistics.clear()

    def reset(self):

        self.clear()

        self.clear_statistics()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self) -> dict:

        return {
            "store": self.store.value,
            "provider": self.embeddings.provider.value,
            "dimensions": self.embeddings.dimensions,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return len(self._chunks)

    def __iter__(self):

        yield from self.configuration().items()