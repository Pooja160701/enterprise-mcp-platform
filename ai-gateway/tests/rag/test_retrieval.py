from __future__ import annotations

import pytest

from app.rag.embeddings import Embeddings
from app.rag.models import (
    ChunkMetadata,
    DocumentChunk,
    RetrievalRequest,
)
from app.rag.retrieval import RetrievalEngine
from app.rag.vector_store import VectorStore


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def embeddings():
    return Embeddings(dimensions=16)


@pytest.fixture
def vector_store(embeddings):
    return VectorStore(embeddings)


@pytest.fixture
def retrieval_engine(embeddings, vector_store):
    return RetrievalEngine(
        embeddings=embeddings,
        vector_store=vector_store,
    )


@pytest.fixture
def populated_store(vector_store):
    chunks = [
        DocumentChunk(
            id="chunk1",
            document_id="doc1",
            text="Python programming language",
            metadata=ChunkMetadata(
                document_id="doc1",
                filename="python.txt",
                chunk_index=0,
                source="tutorial",
            ),
        ),
        DocumentChunk(
            id="chunk2",
            document_id="doc1",
            text="Machine learning with Python",
            metadata=ChunkMetadata(
                document_id="doc1",
                filename="ml.txt",
                chunk_index=1,
                source="book",
            ),
        ),
        DocumentChunk(
            id="chunk3",
            document_id="doc2",
            text="Docker and Kubernetes",
            metadata=ChunkMetadata(
                document_id="doc2",
                filename="devops.txt",
                chunk_index=0,
                source="tutorial",
            ),
        ),
    ]

    vector_store.add(chunks)

    return vector_store


@pytest.fixture
def populated_engine(embeddings, populated_store):
    return RetrievalEngine(
        embeddings,
        populated_store,
    )


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------


def test_initialization(retrieval_engine):
    assert retrieval_engine.embeddings is not None
    assert retrieval_engine.vector_store is not None


# ---------------------------------------------------------
# Retrieve
# ---------------------------------------------------------


def test_retrieve(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
        )
    )

    assert len(results) > 0


def test_retrieve_top_k(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            top_k=2,
        )
    )

    assert len(results) <= 2


def test_retrieve_empty_store(retrieval_engine):
    results = retrieval_engine.retrieve(
        RetrievalRequest(
            query="anything",
        )
    )

    assert results == []


def test_retrieve_unknown_query(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="xxxxxxxxxxxxxxxx",
        )
    )

    assert isinstance(results, list)


# ---------------------------------------------------------
# Metadata Filtering
# ---------------------------------------------------------


def test_filter_source(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            filters={
                "source": "tutorial",
            },
        )
    )

    assert len(results) > 0

    for result in results:
        assert (
            result.chunk.metadata.source
            == "tutorial"
        )


def test_filter_filename(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            filters={
                "filename": "python.txt",
            },
        )
    )

    for result in results:
        assert (
            result.chunk.metadata.filename
            == "python.txt"
        )


def test_filter_document_id(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            filters={
                "document_id": "doc1",
            },
        )
    )

    for result in results:
        assert (
            result.chunk.document_id
            == "doc1"
        )


def test_filter_no_match(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            filters={
                "source": "missing",
            },
        )
    )

    assert results == []


def test_apply_filters_direct(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            top_k=10,
        )
    )

    filtered = populated_engine._apply_filters(
        results,
        {
            "source": "tutorial",
        },
    )

    for result in filtered:
        assert (
            result.chunk.metadata.source
            == "tutorial"
        )


# ---------------------------------------------------------
# Best
# ---------------------------------------------------------


def test_best(populated_engine):
    result = populated_engine.best(
        "Python"
    )

    assert result is not None


def test_best_empty(retrieval_engine):
    assert (
        retrieval_engine.best("hello")
        is None
    )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(populated_engine):
    populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
        )
    )

    stats = populated_engine.statistics()

    assert stats["queries"] == 1
    assert stats["returned"] > 0


def test_multiple_queries(populated_engine):
    for _ in range(5):
        populated_engine.retrieve(
            RetrievalRequest(
                query="Python",
            )
        )

    stats = populated_engine.statistics()

    assert stats["queries"] == 5


def test_clear_statistics(populated_engine):
    populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
        )
    )

    populated_engine.clear_statistics()

    assert (
        populated_engine.statistics()
        == {}
    )


def test_reset(populated_engine):
    populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
        )
    )

    populated_engine.reset()

    assert (
        populated_engine.statistics()
        == {}
    )


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(populated_engine):
    config = populated_engine.configuration()

    assert (
        config["embedding_provider"]
        == "mock"
    )

    assert (
        config["vector_store"]
        == "memory"
    )


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(populated_engine):
    assert len(populated_engine) == 3


def test_iter(populated_engine):
    config = dict(populated_engine)

    assert (
        config["embedding_provider"]
        == "mock"
    )

    assert (
        config["vector_store"]
        == "memory"
    )


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode_query(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="தமிழ் 😀 日本語",
        )
    )

    assert isinstance(results, list)


# ---------------------------------------------------------
# Large Query
# ---------------------------------------------------------


def test_large_query(populated_engine):
    query = "Python " * 5000

    results = populated_engine.retrieve(
        RetrievalRequest(
            query=query,
        )
    )

    assert isinstance(results, list)


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_zero_top_k(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            top_k=0,
        )
    )

    assert results == []


def test_large_top_k(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            top_k=100,
        )
    )

    assert len(results) <= 3


def test_multiple_filters(populated_engine):
    results = populated_engine.retrieve(
        RetrievalRequest(
            query="Python",
            filters={
                "document_id": "doc1",
                "source": "tutorial",
            },
        )
    )

    for result in results:
        metadata = result.chunk.metadata

        assert metadata.document_id == "doc1"
        assert metadata.source == "tutorial"