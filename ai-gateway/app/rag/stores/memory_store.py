from __future__ import annotations

from ..embeddings import Embeddings
from ..models import (
    DocumentChunk,
    RetrievalResult,
    VectorStoreStats,
    VectorStoreType,
)


class MemoryStore:
    """
    Production-ready in-memory vector store.

    Responsibilities
    ----------------
    - Store document chunks
    - Automatically generate embeddings
    - Similarity search
    - CRUD operations
    - Statistics

    Designed as the reference implementation for
    all future vector stores (Chroma, FAISS,
    Pinecone, Qdrant, etc.).
    """

    def __init__(
        self,
        embeddings: Embeddings,
    ):

        self.embeddings = embeddings

        self._chunks: dict[str, DocumentChunk] = {}

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def add(
        self,
        chunks: list[DocumentChunk],
    ) -> None:

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

    def get(
        self,
        chunk_id: str,
    ) -> DocumentChunk | None:

        return self._chunks.get(chunk_id)

    def delete(
        self,
        chunk_id: str,
    ) -> bool:

        if chunk_id not in self._chunks:
            return False

        del self._chunks[chunk_id]

        self._statistics["deleted"] = (
            self._statistics.get("deleted", 0)
            + 1
        )

        return True

    def update(
        self,
        chunk: DocumentChunk,
    ) -> None:

        if not chunk.embedding:

            chunk.embedding = self.embeddings.embed_query(
                chunk.text
            )

        self._chunks[chunk.id] = chunk

        self._statistics["updated"] = (
            self._statistics.get("updated", 0)
            + 1
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

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
            key=lambda result: result.score,
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

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def clear(self) -> None:

        self._chunks.clear()

    def exists(
        self,
        chunk_id: str,
    ) -> bool:

        return chunk_id in self._chunks

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> VectorStoreStats:

        dimensions = 0

        if self._chunks:

            dimensions = len(
                next(
                    iter(self._chunks.values())
                ).embedding
            )

        return VectorStoreStats(
            documents=len(
                {
                    chunk.document_id
                    for chunk in self._chunks.values()
                }
            ),
            chunks=len(self._chunks),
            dimensions=dimensions,
            provider=self.embeddings.provider,
            store=VectorStoreType.MEMORY,
        )

    def runtime_statistics(self) -> dict:

        return dict(self._statistics)

    def clear_statistics(self) -> None:

        self._statistics.clear()

    def reset(self) -> None:

        self.clear()
        self.clear_statistics()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self) -> dict:

        return {
            "store": VectorStoreType.MEMORY.value,
            "provider": self.embeddings.provider.value,
            "dimensions": self.embeddings.dimensions,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return len(self._chunks)

    def __contains__(
        self,
        chunk_id: str,
    ):

        return chunk_id in self._chunks

    def __iter__(self):

        yield from self.configuration().items()