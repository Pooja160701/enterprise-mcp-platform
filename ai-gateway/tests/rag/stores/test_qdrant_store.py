from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.rag.embeddings import Embeddings
from app.rag.models import (
    ChunkMetadata,
    DocumentChunk,
    EmbeddingProvider,
    VectorStoreType,
)
from app.rag.stores.qdrant_store import QdrantStore


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def embeddings():
    return Embeddings(dimensions=16)


@pytest.fixture
def mock_client():
    with patch(
        "app.rag.stores.qdrant_store.QdrantClient"
    ) as client_cls:
        client = MagicMock()

        client.get_collections.return_value = (
            SimpleNamespace(
                collections=[]
            )
        )

        client_cls.return_value = client

        yield client


@pytest.fixture
def store(
    embeddings,
    mock_client,
):
    return QdrantStore(
        embeddings=embeddings,
        collection_name="test_collection",
    )


@pytest.fixture
def chunks():
    return [
        DocumentChunk(
            id=f"chunk{i}",
            document_id="doc1" if i < 2 else "doc2",
            text=f"Chunk {i}",
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


def test_initialization(
    store,
    mock_client,
):
    assert store.collection_name == "test_collection"

    mock_client.create_collection.assert_called_once()


def test_existing_collection(
    embeddings,
):
    with patch(
        "app.rag.stores.qdrant_store.QdrantClient"
    ) as client_cls:
        client = MagicMock()

        client.get_collections.return_value = (
            SimpleNamespace(
                collections=[
                    SimpleNamespace(
                        name="existing"
                    )
                ]
            )
        )

        client_cls.return_value = client

        QdrantStore(
            embeddings,
            collection_name="existing",
        )

        client.create_collection.assert_not_called()


# ---------------------------------------------------------
# Add
# ---------------------------------------------------------


def test_add(
    store,
    chunks,
):
    store.add(chunks)

    store.client.upsert.assert_called_once()

    assert (
        store.runtime_statistics()["added"]
        == 3
    )


def test_add_empty(store):
    store.add([])

    store.client.upsert.assert_not_called()


def test_add_generates_embeddings(
    store,
    chunks,
):
    store.add(chunks)

    for chunk in chunks:
        assert chunk.embedding
        assert len(chunk.embedding) == 16


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------


def test_get_existing(store):
    payload = {
        "document_id": "doc1",
        "filename": "sample.txt",
        "document_type": "text",
        "chunk_index": 0,
        "page": 1,
        "start_char": 0,
        "end_char": 20,
        "source": "manual",
        "extra": {},
        "text": "Hello",
    }

    point = SimpleNamespace(
        id="chunk1",
        vector=[1.0, 2.0],
        payload=payload,
    )

    store.client.retrieve.return_value = [
        point
    ]

    chunk = store.get("chunk1")

    assert chunk.id == "chunk1"
    assert chunk.text == "Hello"


def test_get_missing(store):
    store.client.retrieve.return_value = []

    assert store.get("missing") is None


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------


def test_update(
    store,
    chunks,
):
    store.update(chunks[0])

    assert (
        store.runtime_statistics()["updated"]
        == 1
    )

    store.client.upsert.assert_called_once()


# ---------------------------------------------------------
# Delete
# ---------------------------------------------------------


def test_delete(store):
    assert store.delete("chunk1") is True

    store.client.delete.assert_called_once()

    assert (
        store.runtime_statistics()["deleted"]
        == 1
    )


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------


def test_search(store):
    payload = {
        "document_id": "doc1",
        "filename": "sample.txt",
        "document_type": "text",
        "chunk_index": 0,
        "page": 1,
        "start_char": 0,
        "end_char": 20,
        "source": "manual",
        "extra": {},
        "text": "Hello",
    }

    point = SimpleNamespace(
        id="chunk1",
        vector=[1.0],
        payload=payload,
        score=0.95,
    )

    store.client.search.return_value = [
        point
    ]

    results = store.search([1.0])

    assert len(results) == 1

    assert (
        results[0].chunk.id
        == "chunk1"
    )

    assert results[0].score == pytest.approx(
        0.95
    )


def test_search_empty(store):
    store.client.search.return_value = []

    results = store.search([1.0])

    assert results == []


def test_search_top_k(store):
    payload = {
        "document_id": "doc",
        "filename": "a.txt",
        "document_type": "text",
        "chunk_index": 0,
        "page": None,
        "start_char": 0,
        "end_char": 5,
        "source": None,
        "extra": {},
        "text": "A",
    }

    store.client.search.return_value = [
        SimpleNamespace(
            id="1",
            vector=[1.0],
            payload=payload,
            score=1.0,
        ),
        SimpleNamespace(
            id="2",
            vector=[2.0],
            payload=payload,
            score=0.9,
        ),
    ]

    results = store.search(
        [1.0],
        top_k=2,
    )

    assert len(results) == 2

    store.client.search.assert_called_once()


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(store):
    store.client.get_collection.return_value = (
        SimpleNamespace(
            points_count=10
        )
    )

    stats = store.statistics()

    assert stats.documents == 10
    assert stats.chunks == 10
    assert stats.dimensions == 16
    assert stats.provider == EmbeddingProvider.MOCK
    assert stats.store == VectorStoreType.QDRANT


def test_runtime_statistics(
    store,
):
    store._statistics = {
        "added": 2,
        "searches": 3,
    }

    stats = store.runtime_statistics()

    assert stats["added"] == 2
    assert stats["searches"] == 3


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


def test_clear(store):
    store.clear()

    store.client.delete_collection.assert_called_once_with(
        "test_collection"
    )

    store.client.create_collection.assert_called()


def test_reset(store):
    store._statistics["added"] = 1

    store.reset()

    assert (
        store.runtime_statistics()
        == {}
    )


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(store):
    config = store.configuration()

    assert config["store"] == "qdrant"
    assert (
        config["collection"]
        == "test_collection"
    )
    assert config["provider"] == "mock"
    assert config["dimensions"] == 16


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(store):
    store.client.get_collection.return_value = (
        SimpleNamespace(
            points_count=7
        )
    )

    assert len(store) == 7


def test_iter(store):
    config = dict(store)

    assert config["store"] == "qdrant"
    assert config["provider"] == "mock"


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode(store):
    payload = {
        "document_id": "doc",
        "filename": "unicode.txt",
        "document_type": "text",
        "chunk_index": 0,
        "page": None,
        "start_char": 0,
        "end_char": 5,
        "source": None,
        "extra": {},
        "text": "தமிழ் 😀 日本語",
    }

    point = SimpleNamespace(
        id="unicode",
        vector=[1.0],
        payload=payload,
        score=1.0,
    )

    store.client.search.return_value = [
        point
    ]

    results = store.search([1.0])

    assert (
        results[0].chunk.text
        == "தமிழ் 😀 日本語"
    )


# ---------------------------------------------------------
# Large Result Set
# ---------------------------------------------------------


def test_large_search(store):
    payload = {
        "document_id": "doc",
        "filename": "large.txt",
        "document_type": "text",
        "chunk_index": 0,
        "page": None,
        "start_char": 0,
        "end_char": 10,
        "source": None,
        "extra": {},
        "text": "chunk",
    }

    store.client.search.return_value = [
        SimpleNamespace(
            id=f"id{i}",
            vector=[float(i)],
            payload=payload,
            score=1.0,
        )
        for i in range(100)
    ]

    results = store.search(
        [1.0],
        top_k=100,
    )

    assert len(results) == 100


# ---------------------------------------------------------
# API Errors
# ---------------------------------------------------------


def test_add_error(
    store,
    chunks,
):
    store.client.upsert.side_effect = RuntimeError(
        "Qdrant Error"
    )

    with pytest.raises(RuntimeError):
        store.add(chunks)


def test_search_error(store):
    store.client.search.side_effect = RuntimeError(
        "Search Error"
    )

    with pytest.raises(RuntimeError):
        store.search([1.0])


def test_get_error(store):
    store.client.retrieve.side_effect = RuntimeError(
        "Retrieve Error"
    )

    with pytest.raises(RuntimeError):
        store.get("chunk1")