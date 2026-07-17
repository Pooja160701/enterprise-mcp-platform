from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.rag.embeddings import Embeddings
from app.rag.models import (
    ChunkMetadata,
    DocumentChunk,
    EmbeddingProvider,
    VectorStoreType,
)
from app.rag.stores.chroma_store import ChromaStore


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_collection():
    return MagicMock()


@pytest.fixture
def mock_client(mock_collection):
    with patch(
        "app.rag.stores.chroma_store.Client"
    ) as client_cls:
        client = MagicMock()
        client.get_or_create_collection.return_value = (
            mock_collection
        )
        client_cls.return_value = client
        yield client


@pytest.fixture
def embeddings():
    return Embeddings(dimensions=16)


@pytest.fixture
def store(
    embeddings,
    mock_client,
):
    return ChromaStore(
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


def test_initialization(store):
    assert store.collection_name == "test_collection"


def test_persistent_initialization(
    embeddings,
):
    with patch(
        "app.rag.stores.chroma_store.Client"
    ) as client_cls:
        client = MagicMock()
        client.get_or_create_collection.return_value = (
            MagicMock()
        )
        client_cls.return_value = client

        ChromaStore(
            embeddings,
            persist_directory="/tmp/chroma",
        )

        client_cls.assert_called_once()


# ---------------------------------------------------------
# Add
# ---------------------------------------------------------


def test_add(
    store,
    chunks,
):
    store.add(chunks)

    store.collection.add.assert_called_once()

    assert (
        store.runtime_statistics()["added"]
        == 3
    )


def test_add_empty(store):
    store.add([])

    store.collection.add.assert_not_called()


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
    store.collection.get.return_value = {
        "ids": ["chunk1"],
        "documents": ["hello"],
        "embeddings": [[1.0, 2.0]],
        "metadatas": [
            {
                "document_id": "doc1",
                "filename": "a.txt",
            }
        ],
    }

    chunk = store.get("chunk1")

    assert chunk.id == "chunk1"
    assert chunk.text == "hello"


def test_get_missing(store):
    store.collection.get.return_value = {
        "ids": [],
        "documents": [],
        "embeddings": [],
        "metadatas": [],
    }

    assert store.get("missing") is None


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------


def test_update(
    store,
    chunks,
):
    store.update(chunks[0])

    store.collection.update.assert_called_once()

    assert (
        store.runtime_statistics()["updated"]
        == 1
    )


def test_update_generates_embedding(
    store,
):
    chunk = DocumentChunk(
        id="new",
        document_id="doc",
        text="hello",
        metadata=ChunkMetadata(
            document_id="doc",
            filename="a.txt",
        ),
    )

    store.update(chunk)

    assert chunk.embedding


# ---------------------------------------------------------
# Delete
# ---------------------------------------------------------


def test_delete(store):
    assert store.delete("chunk1") is True

    store.collection.delete.assert_called_once_with(
        ids=["chunk1"]
    )

    assert (
        store.runtime_statistics()["deleted"]
        == 1
    )


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------


def test_search(store):
    store.collection.query.return_value = {
        "ids": [["chunk1"]],
        "documents": [["hello"]],
        "embeddings": [[[1.0, 2.0]]],
        "metadatas": [[
            {
                "document_id": "doc1",
                "filename": "a.txt",
            }
        ]],
        "distances": [[0.2]],
    }

    results = store.search(
        [0.1, 0.2],
    )

    assert len(results) == 1

    assert (
        results[0].chunk.id
        == "chunk1"
    )

    assert results[0].score == pytest.approx(
        0.8
    )


def test_search_empty(store):
    store.collection.query.return_value = {
        "ids": [[]],
        "documents": [[]],
        "embeddings": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }

    results = store.search(
        [0.1],
    )

    assert results == []


def test_search_top_k(store):
    store.collection.query.return_value = {
        "ids": [["a", "b"]],
        "documents": [["A", "B"]],
        "embeddings": [[[1.0], [2.0]]],
        "metadatas": [[
            {
                "document_id": "1",
            },
            {
                "document_id": "2",
            },
        ]],
        "distances": [[0.1, 0.3]],
    }

    results = store.search(
        [0.1],
        top_k=2,
    )

    assert len(results) == 2

    store.collection.query.assert_called_once()


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    store,
):
    store.collection.count.return_value = 5

    stats = store.statistics()

    assert stats.documents == 5
    assert stats.chunks == 5
    assert stats.dimensions == 16
    assert stats.provider == EmbeddingProvider.MOCK
    assert stats.store == VectorStoreType.CHROMA


def test_runtime_statistics(
    store,
):
    store._statistics = {
        "added": 1,
        "searches": 2,
    }

    assert (
        store.runtime_statistics()["added"]
        == 1
    )


def test_clear_statistics(
    store,
):
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

    store.client.get_or_create_collection.assert_called()


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

    assert config["store"] == "chroma"
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
    store.collection.count.return_value = 10

    assert len(store) == 10


def test_iter(store):
    config = dict(store)

    assert config["store"] == "chroma"
    assert config["provider"] == "mock"


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode(store):
    store.collection.query.return_value = {
        "ids": [["unicode"]],
        "documents": [["தமிழ் 😀"]],
        "embeddings": [[[1.0]]],
        "metadatas": [[
            {
                "document_id": "doc",
                "filename": "unicode.txt",
            }
        ]],
        "distances": [[0.0]],
    }

    results = store.search([1.0])

    assert results[0].chunk.text == "தமிழ் 😀"


# ---------------------------------------------------------
# Large Result Set
# ---------------------------------------------------------


def test_large_search(store):
    count = 100

    store.collection.query.return_value = {
        "ids": [[f"id{i}" for i in range(count)]],
        "documents": [[f"text{i}" for i in range(count)]],
        "embeddings": [[[float(i)] for i in range(count)]],
        "metadatas": [[
            {
                "document_id": f"doc{i}",
            }
            for i in range(count)
        ]],
        "distances": [[0.1] * count],
    }

    results = store.search(
        [1.0],
        top_k=count,
    )

    assert len(results) == count


# ---------------------------------------------------------
# API Errors
# ---------------------------------------------------------


def test_add_error(store, chunks):
    store.collection.add.side_effect = RuntimeError(
        "Chroma Error"
    )

    with pytest.raises(RuntimeError):
        store.add(chunks)


def test_query_error(store):
    store.collection.query.side_effect = RuntimeError(
        "Query Error"
    )

    with pytest.raises(RuntimeError):
        store.search([1.0])