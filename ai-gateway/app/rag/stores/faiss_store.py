from __future__ import annotations

import faiss
import numpy as np

from ..embeddings import Embeddings
from ..models import (
    ChunkMetadata,
    DocumentChunk,
    RetrievalResult,
    VectorStoreStats,
    VectorStoreType,
)


class FAISSStore:
    """
    Production-ready FAISS vector store.

    Responsibilities
    ----------------
    - Store document chunks
    - Automatic embedding generation
    - Fast similarity search
    - CRUD operations
    - FAISS index management

    Uses IndexFlatIP (cosine similarity on normalized vectors).
    """

    def __init__(
        self,
        embeddings: Embeddings,
    ):

        self.embeddings = embeddings

        self.dimension = embeddings.dimensions

        self.index = faiss.IndexFlatIP(self.dimension)

        self._chunks: dict[int, DocumentChunk] = {}

        self._id_to_position: dict[str, int] = {}

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def add(
        self,
        chunks: list[DocumentChunk],
    ) -> None:

        if not chunks:
            return

        vectors = []

        for chunk in chunks:

            if not chunk.embedding:

                chunk.embedding = self.embeddings.embed_query(
                    chunk.text
                )

            vector = np.asarray(
                chunk.embedding,
                dtype=np.float32,
            )

            vectors.append(vector)

            position = len(self._chunks)

            self._chunks[position] = chunk

            self._id_to_position[chunk.id] = position

        vectors = np.vstack(vectors)

        faiss.normalize_L2(vectors)

        self.index.add(vectors)

        self._statistics["added"] = (
            self._statistics.get("added", 0)
            + len(chunks)
        )

    def get(
        self,
        chunk_id: str,
    ) -> DocumentChunk | None:

        position = self._id_to_position.get(chunk_id)

        if position is None:
            return None

        return self._chunks[position]

    def delete(
        self,
        chunk_id: str,
    ) -> bool:
        """
        FAISS Flat indexes do not support true deletion.

        Instead we mark the entry as deleted.
        """

        position = self._id_to_position.pop(
            chunk_id,
            None,
        )

        if position is None:
            return False

        del self._chunks[position]

        self._statistics["deleted"] = (
            self._statistics.get("deleted", 0)
            + 1
        )

        return True

    def update(
        self,
        chunk: DocumentChunk,
    ) -> None:

        self.delete(chunk.id)

        self.add([chunk])

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

        if len(self._chunks) == 0:
            return []

        query = np.asarray(
            [query_embedding],
            dtype=np.float32,
        )

        faiss.normalize_L2(query)

        scores, indices = self.index.search(
            query,
            min(top_k, len(self._chunks)),
        )

        results: list[RetrievalResult] = []

        for score, idx in zip(
            scores[0],
            indices[0],
        ):

            if idx == -1:
                continue

            chunk = self._chunks.get(idx)

            if chunk is None:
                continue

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    score=float(score),
                )
            )

        self._statistics["searches"] = (
            self._statistics.get("searches", 0)
            + 1
        )

        self._statistics["returned"] = (
            self._statistics.get("returned", 0)
            + len(results)
        )

        return results

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def clear(self):

        self.index.reset()

        self._chunks.clear()

        self._id_to_position.clear()

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> VectorStoreStats:

        return VectorStoreStats(
            documents=len(
                {
                    chunk.document_id
                    for chunk in self._chunks.values()
                }
            ),
            chunks=len(self._chunks),
            dimensions=self.dimension,
            provider=self.embeddings.provider,
            store=VectorStoreType.FAISS,
        )

    def runtime_statistics(self):

        return dict(self._statistics)

    def clear_statistics(self):

        self._statistics.clear()

    def reset(self):

        self.clear()

        self.clear_statistics()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self):

        return {
            "store": VectorStoreType.FAISS.value,
            "index_type": "IndexFlatIP",
            "dimensions": self.dimension,
            "provider": self.embeddings.provider.value,
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

        return chunk_id in self._id_to_position

    def __iter__(self):

        yield from self.configuration().items()