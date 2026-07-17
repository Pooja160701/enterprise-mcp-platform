from __future__ import annotations

import math

import pytest

from app.rag.models import (
    EmbeddingProvider,
    EmbeddingRequest,
)
from app.rag.providers.mock_embeddings import MockEmbeddings


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def embeddings():
    return MockEmbeddings()


@pytest.fixture
def small_embeddings():
    return MockEmbeddings(dimensions=8)


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------


def test_default_initialization(embeddings):
    assert embeddings.dimensions == 384


def test_custom_initialization():
    model = MockEmbeddings(dimensions=128)

    assert model.dimensions == 128


@pytest.mark.parametrize(
    "dimensions",
    [
        0,
        -1,
        -100,
    ],
)
def test_invalid_dimensions(dimensions):
    with pytest.raises(ValueError):
        MockEmbeddings(dimensions=dimensions)


# ---------------------------------------------------------
# Embed
# ---------------------------------------------------------


def test_embed_single_text(embeddings):
    response = embeddings.embed(
        EmbeddingRequest(
            texts=["hello"],
        )
    )

    assert response.provider == EmbeddingProvider.MOCK
    assert response.dimensions == 384
    assert len(response.embeddings) == 1
    assert len(response.embeddings[0]) == 384


def test_embed_multiple_texts(embeddings):
    response = embeddings.embed(
        EmbeddingRequest(
            texts=[
                "hello",
                "world",
                "python",
            ],
        )
    )

    assert len(response.embeddings) == 3


def test_embed_empty_request(embeddings):
    response = embeddings.embed(
        EmbeddingRequest(
            texts=[],
        )
    )

    assert response.embeddings == []


# ---------------------------------------------------------
# Query Embeddings
# ---------------------------------------------------------


def test_embed_query(embeddings):
    vector = embeddings.embed_query("hello")

    assert len(vector) == 384


def test_empty_query(embeddings):
    vector = embeddings.embed_query("")

    assert vector == [0.0] * 384


# ---------------------------------------------------------
# Deterministic Behaviour
# ---------------------------------------------------------


def test_same_input_same_embedding(
    embeddings,
):
    first = embeddings.embed_query("python")
    second = embeddings.embed_query("python")

    assert first == second


def test_different_input_different_embedding(
    embeddings,
):
    first = embeddings.embed_query("python")
    second = embeddings.embed_query("docker")

    assert first != second


def test_batch_matches_individual(
    embeddings,
):
    texts = [
        "alpha",
        "beta",
        "gamma",
    ]

    batch = embeddings.embed(
        EmbeddingRequest(texts=texts)
    )

    for text, vector in zip(
        texts,
        batch.embeddings,
    ):
        assert vector == embeddings.embed_query(text)


# ---------------------------------------------------------
# Normalization
# ---------------------------------------------------------


def test_embeddings_are_normalized(
    embeddings,
):
    vector = embeddings.embed_query(
        "normalize"
    )

    norm = math.sqrt(
        sum(v * v for v in vector)
    )

    assert norm == pytest.approx(
        1.0,
        rel=1e-6,
    )


def test_normalize_zero_vector():
    vector = [0.0] * 5

    assert (
        MockEmbeddings._normalize(vector)
        == vector
    )


def test_normalize_vector():
    vector = [3.0, 4.0]

    normalized = MockEmbeddings._normalize(
        vector
    )

    norm = math.sqrt(
        sum(v * v for v in normalized)
    )

    assert norm == pytest.approx(1.0)


# ---------------------------------------------------------
# Cosine Similarity
# ---------------------------------------------------------


def test_cosine_similarity_identical(
    embeddings,
):
    vector = embeddings.embed_query("hello")

    similarity = (
        MockEmbeddings.cosine_similarity(
            vector,
            vector,
        )
    )

    assert similarity == pytest.approx(
        1.0,
        rel=1e-6,
    )


def test_cosine_similarity_different(
    embeddings,
):
    a = embeddings.embed_query("hello")
    b = embeddings.embed_query("world")

    similarity = (
        MockEmbeddings.cosine_similarity(
            a,
            b,
        )
    )

    assert -1.0 <= similarity <= 1.0


def test_cosine_similarity_zero_vectors():
    vector = [0.0] * 10

    similarity = (
        MockEmbeddings.cosine_similarity(
            vector,
            vector,
        )
    )

    assert similarity == 0.0


def test_cosine_similarity_dimension_mismatch():
    with pytest.raises(ValueError):
        MockEmbeddings.cosine_similarity(
            [1.0],
            [1.0, 2.0],
        )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(embeddings):
    embeddings.embed(
        EmbeddingRequest(
            texts=["a", "b"],
        )
    )

    embeddings.embed_query("query")

    stats = embeddings.statistics()

    assert stats["requests"] == 1
    assert stats["texts"] == 2
    assert stats["queries"] == 3
    # 2 queries from embed()
    # 1 explicit embed_query()


def test_clear_statistics(
    embeddings,
):
    embeddings.embed(
        EmbeddingRequest(
            texts=["hello"],
        )
    )

    embeddings.clear_statistics()

    assert embeddings.statistics() == {}


def test_reset(embeddings):
    embeddings.embed_query("hello")

    embeddings.reset()

    assert embeddings.statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    embeddings,
):
    config = embeddings.configuration()

    assert config["provider"] == "mock"
    assert config["dimensions"] == 384
    assert config["deterministic"] is True


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(embeddings):
    assert len(embeddings) == 384


def test_iter(embeddings):
    config = dict(embeddings)

    assert config["provider"] == "mock"
    assert config["dimensions"] == 384


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "தமிழ்",
        "日本語",
        "😀 Emoji",
        "مرحبا",
        "हिन्दी",
    ],
)
def test_unicode(
    embeddings,
    text,
):
    vector = embeddings.embed_query(text)

    assert len(vector) == 384


# ---------------------------------------------------------
# Large Input
# ---------------------------------------------------------


def test_large_input(
    embeddings,
):
    text = "hello " * 10000

    vector = embeddings.embed_query(text)

    assert len(vector) == 384


# ---------------------------------------------------------
# Small Dimensions
# ---------------------------------------------------------


def test_small_dimensions(
    small_embeddings,
):
    vector = small_embeddings.embed_query(
        "hello"
    )

    assert len(vector) == 8


# ---------------------------------------------------------
# Value Range
# ---------------------------------------------------------


def test_embedding_value_range(
    embeddings,
):
    vector = embeddings.embed_query(
        "range test"
    )

    assert all(
        -1.0 <= value <= 1.0
        for value in vector
    )