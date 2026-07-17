from __future__ import annotations

import pytest

from app.rag.embeddings import Embeddings
from app.rag.models import (
    ChunkMetadata,
    DocumentChunk,
    EmbeddingProvider,
    VectorStoreType,
)
from app.rag.stores.memory_store import MemoryStore


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def embeddings():
    return Embeddings(dimensions=16)


@pytest.fixture
def store(embeddings):
    return MemoryStore(embeddings)


@pytest.fixture
def chunks():
    return [
        DocumentChunk(
            id=f"chunk{i}",
            document_id="doc1" if i < 2 else "doc2",
            text=f"This is chunk {i}",
            metadata=ChunkMetadata(
                document_id="doc1" if i < 2 else "doc2",
                filename="sample.txt",
                chunk_index=i,
            ),
        )
        for i in range(3)
    ]


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------


def test_initialization(store):
    assert len(store) == 0


# ---------------------------------------------------------
# Add
# ---------------------------------------------------------


def test_add(store, chunks):
    store.add(chunks)

    assert len(store) == 3


def test_add_generates_embeddings(store, chunks):
    store.add(chunks)

    for chunk in chunks:
        assert chunk.embedding
        assert len(chunk.embedding) == 16


def test_add_empty(store):
    store.add([])

    assert len(store) == 0


def test_add_duplicate(store, chunks):
    store.add([chunks[0]])
    store.add([chunks[0]])

    assert len(store) == 1


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------


def test_get_existing(store, chunks):
    store.add(chunks)

    chunk = store.get("chunk0")

    assert chunk is not None
    assert chunk.id == "chunk0"


def test_get_missing(store):
    assert store.get("missing") is None


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------


def test_update_existing(store, chunks):
    store.add(chunks)

    updated = DocumentChunk(
        id="chunk0",
        document_id="doc1",
        text="Updated text",
        metadata=ChunkMetadata(
            document_id="doc1",
            filename="updated.txt",
        ),
    )

    store.update(updated)

    retrieved = store.get("chunk0")

    assert retrieved.text == "Updated text"
    assert retrieved.embedding


def test_update_new_chunk(store):
    chunk = DocumentChunk(
        id="new",
        document_id="doc",
        text="Brand new",
        metadata=ChunkMetadata(
            document_id="doc",
            filename="new.txt",
        ),
    )

    store.update(chunk)

    assert len(store) == 1
    assert store.exists("new")


# ---------------------------------------------------------
# Delete
# ---------------------------------------------------------


def test_delete_existing(store, chunks):
    store.add(chunks)

    assert store.delete("chunk0") is True

    assert len(store) == 2


def test_delete_missing(store):
    assert store.delete("missing") is False


# ---------------------------------------------------------
# Exists
# ---------------------------------------------------------


def test_exists(store, chunks):
    store.add(chunks)

    assert store.exists("chunk0") is True
    assert store.exists("missing") is False


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------


def test_search(store, chunks):
    store.add(chunks)

    query = store.embeddings.embed_query("chunk")

    results = store.search(query)

    assert len(results) > 0


def test_search_top_k(store, chunks):
    store.add(chunks)

    query = store.embeddings.embed_query("chunk")

    results = store.search(
        query,
        top_k=2,
    )

    assert len(results) == 2


def test_search_empty(store):
    query = store.embeddings.embed_query("hello")

    assert store.search(query) == []


def test_search_sorted(store, chunks):
    store.add(chunks)

    query = store.embeddings.embed_query(
        chunks[0].text
    )

    results = store.search(query)

    scores = [r.score for r in results]

    assert scores == sorted(
        scores,
        reverse=True,
    )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(store, chunks):
    store.add(chunks)

    stats = store.statistics()

    assert stats.documents == 2
    assert stats.chunks == 3
    assert stats.dimensions == 16
    assert stats.provider == EmbeddingProvider.MOCK
    assert stats.store == VectorStoreType.MEMORY


def test_empty_statistics(store):
    stats = store.statistics()

    assert stats.documents == 0
    assert stats.chunks == 0
    assert stats.dimensions == 0


def test_runtime_statistics(store, chunks):
    store.add(chunks)

    query = store.embeddings.embed_query("hello")

    store.search(query)

    store.update(chunks[0])

    store.delete("chunk0")

    stats = store.runtime_statistics()

    assert stats["added"] == 3
    assert stats["updated"] == 1
    assert stats["deleted"] == 1
    assert stats["searches"] == 1
    assert stats["returned"] > 0


def test_clear_statistics(store, chunks):
    store.add(chunks)

    store.clear_statistics()

    assert store.runtime_statistics() == {}


# ---------------------------------------------------------
# Clear / Reset
# ---------------------------------------------------------


def test_clear(store, chunks):
    store.add(chunks)

    store.clear()

    assert len(store) == 0


def test_reset(store, chunks):
    store.add(chunks)

    store.reset()

    assert len(store) == 0
    assert store.runtime_statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(store):
    config = store.configuration()

    assert config["store"] == "memory"
    assert config["provider"] == "mock"
    assert config["dimensions"] == 16


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(store, chunks):
    store.add(chunks)

    assert len(store) == 3


def test_contains(store, chunks):
    store.add(chunks)

    assert "chunk0" in store
    assert "missing" not in store


def test_iter(store):
    config = dict(store)

    assert config["store"] == "memory"
    assert config["provider"] == "mock"


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode(store):
    chunk = DocumentChunk(
        id="unicode",
        document_id="doc",
        text="தமிழ் 😀 日本語",
        metadata=ChunkMetadata(
            document_id="doc",
            filename="unicode.txt",
        ),
    )

    store.add([chunk])

    query = store.embeddings.embed_query("தமிழ்")

    results = store.search(query)

    assert len(results) == 1


# ---------------------------------------------------------
# Large Dataset
# ---------------------------------------------------------


def test_large_dataset(store):
    chunks = []

    for i in range(1000):
        chunks.append(
            DocumentChunk(
                id=f"id{i}",
                document_id=f"doc{i // 10}",
                text=f"Chunk {i}",
                metadata=ChunkMetadata(
                    document_id=f"doc{i // 10}",
                    filename="large.txt",
                    chunk_index=i,
                ),
            )
        )

    store.add(chunks)

    assert len(store) == 1000

    query = store.embeddings.embed_query("Chunk")

    results = store.search(
        query,
        top_k=20,
    )

    assert len(results) == 20


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_single_chunk(store):
    chunk = DocumentChunk(
        id="only",
        document_id="doc",
        text="Only chunk",
        metadata=ChunkMetadata(
            document_id="doc",
            filename="one.txt",
        ),
    )

    store.add([chunk])

    query = store.embeddings.embed_query("Only")

    results = store.search(query)

    assert len(results) == 1
    assert results[0].chunk.id == "only"


def test_delete_all(store, chunks):
    store.add(chunks)

    for chunk in chunks:
        assert store.delete(chunk.id)

    assert len(store) == 0


def test_multiple_searches(store, chunks):
    store.add(chunks)

    query = store.embeddings.embed_query("chunk")

    for _ in range(5):
        store.search(query)

    stats = store.runtime_statistics()

    assert stats["searches"] == 5