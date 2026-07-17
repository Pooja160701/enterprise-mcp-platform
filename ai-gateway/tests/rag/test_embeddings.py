from __future__ import annotations

import math

import pytest

from app.rag.embeddings import Embeddings
from app.rag.models import (
    EmbeddingProvider,
    EmbeddingRequest,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def embeddings():
    return Embeddings()


@pytest.fixture
def small_embeddings():
    return Embeddings(
        dimensions=8,
    )


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------


def test_default_initialization(embeddings):
    assert embeddings.provider == EmbeddingProvider.MOCK
    assert embeddings.dimensions == 384


def test_custom_initialization():
    model = Embeddings(
        provider=EmbeddingProvider.OPENAI,
        dimensions=768,
    )

    assert model.provider == EmbeddingProvider.OPENAI
    assert model.dimensions == 768


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
        Embeddings(dimensions=dimensions)


# ---------------------------------------------------------
# Embed
# ---------------------------------------------------------


def test_embed_single_text(embeddings):
    request = EmbeddingRequest(
        texts=["hello"],
    )

    response = embeddings.embed(request)

    assert len(response.embeddings) == 1
    assert len(response.embeddings[0]) == embeddings.dimensions


def test_embed_multiple_texts(embeddings):
    request = EmbeddingRequest(
        texts=[
            "hello",
            "world",
            "python",
        ],
    )

    response = embeddings.embed(request)

    assert len(response.embeddings) == 3


def test_embed_empty_list(embeddings):
    request = EmbeddingRequest(
        texts=[],
    )

    response = embeddings.embed(request)

    assert response.embeddings == []


def test_embed_query(embeddings):
    vector = embeddings.embed_query(
        "search query"
    )

    assert len(vector) == embeddings.dimensions


# ---------------------------------------------------------
# Deterministic Embeddings
# ---------------------------------------------------------


def test_same_text_same_embedding(embeddings):
    first = embeddings.embed_query("hello")
    second = embeddings.embed_query("hello")

    assert first == second


def test_different_texts_different_embeddings(
    embeddings,
):
    first = embeddings.embed_query("hello")
    second = embeddings.embed_query("world")

    assert first != second


def test_empty_string_embedding(embeddings):
    vector = embeddings.embed_query("")

    assert len(vector) == embeddings.dimensions
    assert all(v == 0.0 for v in vector)


# ---------------------------------------------------------
# Normalization
# ---------------------------------------------------------


def test_embedding_is_normalized(embeddings):
    vector = embeddings.embed_query(
        "normalize me"
    )

    norm = math.sqrt(
        sum(x * x for x in vector)
    )

    assert norm == pytest.approx(
        1.0,
        rel=1e-6,
    )


def test_normalize_zero_vector(embeddings):
    vector = [0.0] * 10

    normalized = embeddings._normalize(vector)

    assert normalized == vector


def test_normalize_vector(embeddings):
    vector = [3.0, 4.0]

    normalized = embeddings._normalize(vector)

    norm = math.sqrt(
        sum(x * x for x in normalized)
    )

    assert norm == pytest.approx(1.0)


# ---------------------------------------------------------
# Cosine Similarity
# ---------------------------------------------------------


def test_cosine_similarity_identical(embeddings):
    vector = embeddings.embed_query("hello")

    similarity = embeddings.cosine_similarity(
        vector,
        vector,
    )

    assert similarity == pytest.approx(
        1.0,
        rel=1e-6,
    )


def test_cosine_similarity_different(embeddings):
    a = embeddings.embed_query("hello")
    b = embeddings.embed_query("world")

    similarity = embeddings.cosine_similarity(
        a,
        b,
    )

    assert -1.0 <= similarity <= 1.0


def test_cosine_similarity_zero_vectors(
    embeddings,
):
    vector = [0.0] * embeddings.dimensions

    similarity = embeddings.cosine_similarity(
        vector,
        vector,
    )

    assert similarity == 0.0


def test_cosine_similarity_dimension_mismatch(
    embeddings,
):
    with pytest.raises(ValueError):
        embeddings.cosine_similarity(
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
    assert stats["queries"] == 1


def test_clear_statistics(embeddings):
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


def test_configuration(embeddings):
    config = embeddings.configuration()

    assert config["provider"] == "mock"
    assert config["dimensions"] == 384
    assert (
        config["algorithm"]
        == "deterministic_hash_embedding"
    )


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
def test_unicode_embeddings(
    embeddings,
    text,
):
    vector = embeddings.embed_query(text)

    assert len(vector) == embeddings.dimensions


# ---------------------------------------------------------
# Large Input
# ---------------------------------------------------------


def test_large_text(embeddings):
    text = "hello " * 10000

    vector = embeddings.embed_query(text)

    assert len(vector) == embeddings.dimensions


# ---------------------------------------------------------
# Small Dimensions
# ---------------------------------------------------------


def test_small_dimension_embeddings(
    small_embeddings,
):
    vector = small_embeddings.embed_query(
        "hello"
    )

    assert len(vector) == 8


# ---------------------------------------------------------
# Batch Consistency
# ---------------------------------------------------------


def test_batch_matches_individual(
    embeddings,
):
    texts = [
        "alpha",
        "beta",
        "gamma",
    ]

    response = embeddings.embed(
        EmbeddingRequest(
            texts=texts,
        )
    )

    for text, vector in zip(
        texts,
        response.embeddings,
    ):
        assert (
            vector
            == embeddings.embed_query(text)
        )


# ---------------------------------------------------------
# Response Metadata
# ---------------------------------------------------------


def test_response_metadata(
    embeddings,
):
    response = embeddings.embed(
        EmbeddingRequest(
            texts=["hello"],
        )
    )

    assert (
        response.provider
        == EmbeddingProvider.MOCK
    )
    assert (
        response.dimensions
        == embeddings.dimensions
    )


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