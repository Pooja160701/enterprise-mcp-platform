from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from app.rag.embeddings import Embeddings
from app.rag.models import (
    ChunkMetadata,
    DocumentChunk,
    EmbeddingProvider,
    VectorStoreType,
)
from app.rag.stores.faiss_store import FAISSStore


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def embeddings():
    return Embeddings(dimensions=16)


@pytest.fixture
def mock_index():
    return MagicMock()


@pytest.fixture
def store(embeddings, mock_index):
    with patch(
        "app.rag.stores.faiss_store.faiss.IndexFlatIP",
        return_value=mock_index,
    ):
        return FAISSStore(embeddings)


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
    assert store.dimension == 16
    assert len(store) == 0


# ---------------------------------------------------------
# Add
# ---------------------------------------------------------


def test_add(store, mock_index, chunks):
    store.add(chunks)

    assert len(store) == 3

    mock_index.add.assert_called_once()

    assert (
        store.runtime_statistics()["added"]
        == 3
    )


def test_add_empty(store, mock_index):
    store.add([])

    mock_index.add.assert_not_called()

    assert len(store) == 0


def test_add_generates_embeddings(
    store,
    chunks,
):
    store.add(chunks)

    for chunk in chunks:
        assert chunk.embedding
        assert len(chunk.embedding) == 16


def test_add_duplicate(store, chunks):
    store.add([chunks[0]])
    store.add([chunks[0]])

    assert len(store) == 2


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
# Delete
# ---------------------------------------------------------


def test_delete_existing(store, chunks):
    store.add(chunks)

    assert store.delete("chunk0") is True

    assert "chunk0" not in store

    assert (
        store.runtime_statistics()["deleted"]
        == 1
    )


def test_delete_missing(store):
    assert store.delete("missing") is False


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------


def test_update_existing(store, chunks):
    store.add(chunks)

    updated = DocumentChunk(
        id="chunk0",
        document_id="doc1",
        text="Updated",
        metadata=ChunkMetadata(
            document_id="doc1",
            filename="updated.txt",
        ),
    )

    store.update(updated)

    retrieved = store.get("chunk0")

    assert retrieved.text == "Updated"

    assert (
        store.runtime_statistics()["updated"]
        == 1
    )


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

    assert "new" in store


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------


def test_search(store, mock_index, chunks):
    store.add(chunks)

    mock_index.search.return_value = (
        np.array([[0.95, 0.80]], dtype=np.float32),
        np.array([[0, 1]], dtype=np.int64),
    )

    query = store.embeddings.embed_query(
        "chunk"
    )

    results = store.search(
        query,
        top_k=2,
    )

    assert len(results) == 2

    assert results[0].score == pytest.approx(
        0.95
    )


def test_search_empty(store):
    query = store.embeddings.embed_query(
        "hello"
    )

    assert store.search(query) == []


def test_search_invalid_indices(
    store,
    mock_index,
    chunks,
):
    store.add(chunks)

    mock_index.search.return_value = (
        np.array([[0.9, 0.8]], dtype=np.float32),
        np.array([[-1, 100]], dtype=np.int64),
    )

    query = store.embeddings.embed_query(
        "hello"
    )

    results = store.search(query)

    assert results == []


def test_search_top_k(
    store,
    mock_index,
    chunks,
):
    store.add(chunks)

    mock_index.search.return_value = (
        np.array([[0.9]], dtype=np.float32),
        np.array([[0]], dtype=np.int64),
    )

    query = store.embeddings.embed_query(
        "hello"
    )

    results = store.search(
        query,
        top_k=1,
    )

    assert len(results) == 1

    mock_index.search.assert_called_once()


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
    assert stats.store == VectorStoreType.FAISS


def test_empty_statistics(store):
    stats = store.statistics()

    assert stats.documents == 0
    assert stats.chunks == 0


def test_runtime_statistics(
    store,
    chunks,
):
    store.add(chunks)

    store._statistics["searches"] = 1
    store._statistics["returned"] = 2

    stats = store.runtime_statistics()

    assert stats["added"] == 3
    assert stats["searches"] == 1


def test_clear_statistics(store):
    store._statistics["added"] = 5

    store.clear_statistics()

    assert (
        store.runtime_statistics()
        == {}
    )


# ---------------------------------------------------------
# Clear / Reset
# ---------------------------------------------------------


def test_clear(store, mock_index, chunks):
    store.add(chunks)

    store.clear()

    mock_index.reset.assert_called_once()

    assert len(store) == 0


def test_reset(store, mock_index, chunks):
    store.add(chunks)

    store.reset()

    mock_index.reset.assert_called_once()

    assert len(store) == 0
    assert (
        store.runtime_statistics()
        == {}
    )


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(store):
    config = store.configuration()

    assert config["store"] == "faiss"
    assert (
        config["index_type"]
        == "IndexFlatIP"
    )
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

    assert config["store"] == "faiss"
    assert config["provider"] == "mock"


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode(store, mock_index):
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

    mock_index.search.return_value = (
        np.array([[1.0]], dtype=np.float32),
        np.array([[0]], dtype=np.int64),
    )

    query = store.embeddings.embed_query(
        "தமிழ்"
    )

    results = store.search(query)

    assert len(results) == 1
    assert (
        results[0].chunk.text
        == "தமிழ் 😀 日本語"
    )


# ---------------------------------------------------------
# Large Dataset
# ---------------------------------------------------------


def test_large_dataset(
    store,
    mock_index,
):
    chunks = []

    for i in range(1000):
        chunks.append(
            DocumentChunk(
                id=f"id{i}",
                document_id=f"doc{i//10}",
                text=f"Chunk {i}",
                metadata=ChunkMetadata(
                    document_id=f"doc{i//10}",
                    filename="large.txt",
                ),
            )
        )

    store.add(chunks)

    scores = np.array(
        [[1.0] * 20],
        dtype=np.float32,
    )

    indices = np.array(
        [list(range(20))],
        dtype=np.int64,
    )

    mock_index.search.return_value = (
        scores,
        indices,
    )

    query = store.embeddings.embed_query(
        "Chunk"
    )

    results = store.search(
        query,
        top_k=20,
    )

    assert len(results) == 20


# ---------------------------------------------------------
# FAISS Errors
# ---------------------------------------------------------


def test_add_error(
    store,
    mock_index,
    chunks,
):
    mock_index.add.side_effect = RuntimeError(
        "FAISS Error"
    )

    with pytest.raises(RuntimeError):
        store.add(chunks)


def test_search_error(
    store,
    mock_index,
    chunks,
):
    store.add(chunks)

    mock_index.search.side_effect = RuntimeError(
        "Search Error"
    )

    query = store.embeddings.embed_query(
        "hello"
    )

    with pytest.raises(RuntimeError):
        store.search(query)