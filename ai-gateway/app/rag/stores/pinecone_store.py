from __future__ import annotations

from pinecone import Pinecone, ServerlessSpec

from ..embeddings import Embeddings
from ..models import (
    ChunkMetadata,
    DocumentChunk,
    RetrievalResult,
    VectorStoreStats,
    VectorStoreType,
)


class PineconeStore:
    """
    Production-ready Pinecone vector store.

    Responsibilities
    ----------------
    - Store document chunks
    - Automatic embedding generation
    - CRUD operations
    - Similarity search
    - Index management

    Uses Pinecone Serverless.
    """

    def __init__(
        self,
        embeddings: Embeddings,
        api_key: str,
        index_name: str = "rag-index",
        cloud: str = "aws",
        region: str = "us-east-1",
    ):

        self.embeddings = embeddings
        self.index_name = index_name

        self.pc = Pinecone(api_key=api_key)

        if index_name not in self.pc.list_indexes().names():

            self.pc.create_index(
                name=index_name,
                dimension=embeddings.dimensions,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=cloud,
                    region=region,
                ),
            )

        self.index = self.pc.Index(index_name)

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

            metadata = chunk.metadata.model_dump()

            metadata.update(
                {
                    "document_id": chunk.document_id,
                    "text": chunk.text,
                }
            )

            vectors.append(
                {
                    "id": chunk.id,
                    "values": chunk.embedding,
                    "metadata": metadata,
                }
            )

        self.index.upsert(
            vectors=vectors,
        )

        self._statistics["added"] = (
            self._statistics.get("added", 0)
            + len(chunks)
        )

    def get(
        self,
        chunk_id: str,
    ) -> DocumentChunk | None:

        response = self.index.fetch(
            ids=[chunk_id],
        )

        if chunk_id not in response.vectors:
            return None

        vector = response.vectors[chunk_id]

        metadata = vector.metadata

        chunk_metadata = ChunkMetadata(
            document_id=metadata["document_id"],
            filename=metadata["filename"],
            document_type=metadata["document_type"],
            chunk_index=metadata["chunk_index"],
            page=metadata.get("page"),
            start_char=metadata["start_char"],
            end_char=metadata["end_char"],
            source=metadata.get("source"),
            extra=metadata.get("extra", {}),
        )

        return DocumentChunk(
            id=chunk_id,
            document_id=metadata["document_id"],
            text=metadata["text"],
            embedding=vector.values,
            metadata=chunk_metadata,
        )

    def delete(
        self,
        chunk_id: str,
    ) -> bool:

        self.index.delete(
            ids=[chunk_id],
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

        response = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_values=True,
            include_metadata=True,
        )

        results: list[RetrievalResult] = []

        for match in response.matches:

            metadata = match.metadata

            chunk_metadata = ChunkMetadata(
                document_id=metadata["document_id"],
                filename=metadata["filename"],
                document_type=metadata["document_type"],
                chunk_index=metadata["chunk_index"],
                page=metadata.get("page"),
                start_char=metadata["start_char"],
                end_char=metadata["end_char"],
                source=metadata.get("source"),
                extra=metadata.get("extra", {}),
            )

            chunk = DocumentChunk(
                id=match.id,
                document_id=metadata["document_id"],
                text=metadata["text"],
                embedding=match.values,
                metadata=chunk_metadata,
            )

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    score=float(match.score),
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

        self.index.delete(delete_all=True)

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> VectorStoreStats:

        stats = self.index.describe_index_stats()

        chunks = stats.total_vector_count

        return VectorStoreStats(
            documents=chunks,
            chunks=chunks,
            dimensions=self.embeddings.dimensions,
            provider=self.embeddings.provider,
            store=VectorStoreType.PINECONE,
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
            "store": VectorStoreType.PINECONE.value,
            "index": self.index_name,
            "provider": self.embeddings.provider.value,
            "dimensions": self.embeddings.dimensions,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return self.statistics().chunks

    def __contains__(
        self,
        chunk_id: str,
    ):

        return self.get(chunk_id) is not None

    def __iter__(self):

        yield from self.configuration().items()