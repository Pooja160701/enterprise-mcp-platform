from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from ..embeddings import Embeddings
from ..models import (
    ChunkMetadata,
    DocumentChunk,
    RetrievalResult,
    VectorStoreStats,
    VectorStoreType,
)


class QdrantStore:
    """
    Production-ready Qdrant vector store.

    Responsibilities
    ----------------
    - Store document chunks
    - Automatic embedding generation
    - Vector similarity search
    - CRUD operations
    - Collection management

    Uses cosine similarity.
    """

    def __init__(
        self,
        embeddings: Embeddings,
        collection_name: str = "rag_documents",
        host: str = "localhost",
        port: int = 6333,
        api_key: str | None = None,
    ):

        self.embeddings = embeddings
        self.collection_name = collection_name

        self.client = QdrantClient(
            host=host,
            port=port,
            api_key=api_key,
        )

        collections = [
            collection.name
            for collection in self.client.get_collections().collections
        ]

        if collection_name not in collections:

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=embeddings.dimensions,
                    distance=Distance.COSINE,
                ),
            )

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

        points = []

        for chunk in chunks:

            if not chunk.embedding:

                chunk.embedding = self.embeddings.embed_query(
                    chunk.text
                )

            payload = chunk.metadata.model_dump()

            payload.update(
                {
                    "document_id": chunk.document_id,
                    "text": chunk.text,
                }
            )

            points.append(
                PointStruct(
                    id=chunk.id,
                    vector=chunk.embedding,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )

        self._statistics["added"] = (
            self._statistics.get("added", 0)
            + len(chunks)
        )

    def get(
        self,
        chunk_id: str,
    ) -> DocumentChunk | None:

        result = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[chunk_id],
            with_vectors=True,
        )

        if not result:
            return None

        point = result[0]

        payload = point.payload

        metadata = ChunkMetadata(
            document_id=payload["document_id"],
            filename=payload["filename"],
            document_type=payload["document_type"],
            chunk_index=payload["chunk_index"],
            page=payload.get("page"),
            start_char=payload["start_char"],
            end_char=payload["end_char"],
            source=payload.get("source"),
            extra=payload.get("extra", {}),
        )

        return DocumentChunk(
            id=str(point.id),
            document_id=payload["document_id"],
            text=payload["text"],
            embedding=point.vector,
            metadata=metadata,
        )

    def delete(
        self,
        chunk_id: str,
    ) -> bool:

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[chunk_id],
            wait=True,
        )

        self._statistics["deleted"] = (
            self._statistics.get("deleted", 0)
            + 1
        )

        return True

    def update(
        self,
        chunk: DocumentChunk,
    ) -> None:

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

        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_vectors=True,
            with_payload=True,
        )

        results: list[RetrievalResult] = []

        for point in response:

            payload = point.payload

            metadata = ChunkMetadata(
                document_id=payload["document_id"],
                filename=payload["filename"],
                document_type=payload["document_type"],
                chunk_index=payload["chunk_index"],
                page=payload.get("page"),
                start_char=payload["start_char"],
                end_char=payload["end_char"],
                source=payload.get("source"),
                extra=payload.get("extra", {}),
            )

            chunk = DocumentChunk(
                id=str(point.id),
                document_id=payload["document_id"],
                text=payload["text"],
                embedding=point.vector,
                metadata=metadata,
            )

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    score=float(point.score),
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

        self.client.delete_collection(
            self.collection_name
        )

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.embeddings.dimensions,
                distance=Distance.COSINE,
            ),
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> VectorStoreStats:

        info = self.client.get_collection(
            self.collection_name
        )

        return VectorStoreStats(
            documents=info.points_count,
            chunks=info.points_count,
            dimensions=self.embeddings.dimensions,
            provider=self.embeddings.provider,
            store=VectorStoreType.QDRANT,
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
            "store": VectorStoreType.QDRANT.value,
            "collection": self.collection_name,
            "provider": self.embeddings.provider.value,
            "dimensions": self.embeddings.dimensions,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return self.statistics().chunks

    def __iter__(self):

        yield from self.configuration().items()