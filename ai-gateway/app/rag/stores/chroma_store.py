from __future__ import annotations

from chromadb import Client
from chromadb.config import Settings

from ..embeddings import Embeddings
from ..models import (
    DocumentChunk,
    RetrievalResult,
    VectorStoreStats,
    VectorStoreType,
)


class ChromaStore:
    """
    Production-ready ChromaDB vector store.

    Responsibilities
    ----------------
    - Store document chunks
    - Automatic embedding generation
    - Similarity search
    - CRUD operations
    - Collection management

    Uses ChromaDB as the storage backend.
    """

    def __init__(
        self,
        embeddings: Embeddings,
        collection_name: str = "rag_documents",
        persist_directory: str | None = None,
    ):

        self.embeddings = embeddings

        if persist_directory:

            self.client = Client(
                Settings(
                    is_persistent=True,
                    persist_directory=persist_directory,
                )
            )

        else:

            self.client = Client()

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
        )

        self.collection_name = collection_name

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

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:

            if not chunk.embedding:

                chunk.embedding = self.embeddings.embed_query(
                    chunk.text
                )

            ids.append(chunk.id)

            documents.append(chunk.text)

            embeddings.append(chunk.embedding)

            metadata = chunk.metadata.model_dump()

            metadata["document_id"] = chunk.document_id

            metadatas.append(metadata)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        self._statistics["added"] = (
            self._statistics.get("added", 0)
            + len(chunks)
        )

    def get(
        self,
        chunk_id: str,
    ):

        result = self.collection.get(
            ids=[chunk_id],
            include=[
                "documents",
                "embeddings",
                "metadatas",
            ],
        )

        if not result["ids"]:
            return None

        metadata = result["metadatas"][0]

        return DocumentChunk(
            id=result["ids"][0],
            document_id=metadata["document_id"],
            text=result["documents"][0],
            embedding=result["embeddings"][0],
            metadata=metadata,
        )

    def delete(
        self,
        chunk_id: str,
    ) -> bool:

        self.collection.delete(
            ids=[chunk_id]
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

        if not chunk.embedding:

            chunk.embedding = self.embeddings.embed_query(
                chunk.text
            )

        metadata = chunk.metadata.model_dump()

        metadata["document_id"] = chunk.document_id

        self.collection.update(
            ids=[chunk.id],
            documents=[chunk.text],
            embeddings=[chunk.embedding],
            metadatas=[metadata],
        )

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

        response = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "embeddings",
                "metadatas",
                "distances",
            ],
        )

        results: list[RetrievalResult] = []

        ids = response["ids"][0]
        docs = response["documents"][0]
        embeds = response["embeddings"][0]
        metas = response["metadatas"][0]
        distances = response["distances"][0]

        for idx in range(len(ids)):

            metadata = metas[idx]

            chunk = DocumentChunk(
                id=ids[idx],
                document_id=metadata["document_id"],
                text=docs[idx],
                embedding=embeds[idx],
                metadata=metadata,
            )

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    score=1.0 - distances[idx],
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

        self.collection = (
            self.client.get_or_create_collection(
                self.collection_name
            )
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> VectorStoreStats:

        count = self.collection.count()

        return VectorStoreStats(
            documents=count,
            chunks=count,
            dimensions=self.embeddings.dimensions,
            provider=self.embeddings.provider,
            store=VectorStoreType.CHROMA,
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
            "store": VectorStoreType.CHROMA.value,
            "collection": self.collection_name,
            "provider": self.embeddings.provider.value,
            "dimensions": self.embeddings.dimensions,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return self.collection.count()

    def __iter__(self):

        yield from self.configuration().items()