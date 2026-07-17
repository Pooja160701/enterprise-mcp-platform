from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.rag.models import (
    EmbeddingProvider,
    EmbeddingRequest,
)
from app.rag.providers.sentence_transformers import (
    SentenceTransformerEmbeddings,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_model():
    with patch(
        "app.rag.providers.sentence_transformers.SentenceTransformer"
    ) as model_cls:
        model = MagicMock()
        model_cls.return_value = model

        model.get_sentence_embedding_dimension.return_value = 384

        yield model


@pytest.fixture
def provider(mock_model):
    return SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2",
    )


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


class FakeEmbedding:
    def __init__(self, value):
        self.value = value

    def tolist(self):
        return self.value


class FakeEmbeddings:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return self.values


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------


def test_initialization(provider):
    assert provider.model_name == "all-MiniLM-L6-v2"


def test_custom_model(mock_model):
    provider = SentenceTransformerEmbeddings(
        model_name="bge-small-en-v1.5",
        device="cpu",
    )

    assert provider.model_name == "bge-small-en-v1.5"


# ---------------------------------------------------------
# Embed
# ---------------------------------------------------------


def test_embed(provider, mock_model):
    mock_model.encode.return_value = FakeEmbeddings(
        [
            [0.1, 0.2],
            [0.3, 0.4],
        ]
    )

    response = provider.embed(
        EmbeddingRequest(
            texts=[
                "hello",
                "world",
            ]
        )
    )

    assert (
        response.provider
        == EmbeddingProvider.SENTENCE_TRANSFORMERS
    )

    assert response.dimensions == 2
    assert len(response.embeddings) == 2


def test_embed_empty(provider, mock_model):
    mock_model.encode.return_value = FakeEmbeddings([])

    response = provider.embed(
        EmbeddingRequest(texts=[])
    )

    assert response.embeddings == []
    assert response.dimensions == 0


def test_embed_calls_model(provider, mock_model):
    mock_model.encode.return_value = FakeEmbeddings(
        [[1.0]]
    )

    provider.embed(
        EmbeddingRequest(
            texts=["hello"]
        )
    )

    mock_model.encode.assert_called_once_with(
        ["hello"],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )


# ---------------------------------------------------------
# Query Embedding
# ---------------------------------------------------------


def test_embed_query(provider, mock_model):
    mock_model.encode.return_value = FakeEmbedding(
        [1.0, 2.0, 3.0]
    )

    vector = provider.embed_query("hello")

    assert vector == [1.0, 2.0, 3.0]


def test_embed_query_calls_model(
    provider,
    mock_model,
):
    mock_model.encode.return_value = FakeEmbedding(
        [0.5]
    )

    provider.embed_query("query")

    mock_model.encode.assert_called_once_with(
        "query",
        convert_to_numpy=True,
        normalize_embeddings=True,
    )


# ---------------------------------------------------------
# Cosine Similarity
# ---------------------------------------------------------


def test_cosine_similarity_identical():
    vector = [1.0, 2.0, 3.0]

    similarity = (
        SentenceTransformerEmbeddings.cosine_similarity(
            vector,
            vector,
        )
    )

    assert similarity == pytest.approx(1.0)


def test_cosine_similarity_different():
    similarity = (
        SentenceTransformerEmbeddings.cosine_similarity(
            [1.0, 0.0],
            [0.0, 1.0],
        )
    )

    assert similarity == pytest.approx(0.0)


def test_cosine_similarity_zero_vector():
    similarity = (
        SentenceTransformerEmbeddings.cosine_similarity(
            [0.0, 0.0],
            [0.0, 0.0],
        )
    )

    assert similarity == 0.0


def test_cosine_similarity_dimension_mismatch():
    with pytest.raises(ValueError):
        SentenceTransformerEmbeddings.cosine_similarity(
            [1.0],
            [1.0, 2.0],
        )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(provider, mock_model):
    mock_model.encode.side_effect = [
        FakeEmbeddings([[1.0], [2.0]]),
        FakeEmbedding([3.0]),
    ]

    provider.embed(
        EmbeddingRequest(
            texts=[
                "a",
                "b",
            ]
        )
    )

    provider.embed_query("query")

    stats = provider.statistics()

    assert stats["requests"] == 1
    assert stats["texts"] == 2
    assert stats["queries"] == 1


def test_multiple_requests(
    provider,
    mock_model,
):
    mock_model.encode.return_value = FakeEmbeddings(
        [[1.0]]
    )

    for _ in range(5):
        provider.embed(
            EmbeddingRequest(
                texts=["hello"]
            )
        )

    stats = provider.statistics()

    assert stats["requests"] == 5
    assert stats["texts"] == 5


def test_clear_statistics(
    provider,
    mock_model,
):
    mock_model.encode.return_value = FakeEmbeddings(
        [[1.0]]
    )

    provider.embed(
        EmbeddingRequest(
            texts=["hello"]
        )
    )

    provider.clear_statistics()

    assert provider.statistics() == {}


def test_reset(
    provider,
    mock_model,
):
    mock_model.encode.return_value = FakeEmbedding(
        [1.0]
    )

    provider.embed_query("hello")

    provider.reset()

    assert provider.statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(provider):
    config = provider.configuration()

    assert (
        config["provider"]
        == "sentence_transformers"
    )

    assert (
        config["model"]
        == "all-MiniLM-L6-v2"
    )

    assert config["dimensions"] == 384


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(provider):
    assert len(provider) == 384


def test_iter(provider):
    config = dict(provider)

    assert (
        config["provider"]
        == "sentence_transformers"
    )

    assert (
        config["model"]
        == "all-MiniLM-L6-v2"
    )


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode_query(
    provider,
    mock_model,
):
    mock_model.encode.return_value = FakeEmbedding(
        [0.1]
    )

    vector = provider.embed_query(
        "தமிழ் 😀 日本語"
    )

    assert vector == [0.1]


# ---------------------------------------------------------
# Large Batch
# ---------------------------------------------------------


def test_large_batch(
    provider,
    mock_model,
):
    texts = [
        f"text {i}"
        for i in range(100)
    ]

    vectors = [
        [float(i)]
        for i in range(100)
    ]

    mock_model.encode.return_value = FakeEmbeddings(
        vectors
    )

    response = provider.embed(
        EmbeddingRequest(
            texts=texts
        )
    )

    assert len(response.embeddings) == 100


# ---------------------------------------------------------
# Model Errors
# ---------------------------------------------------------


def test_embed_model_error(
    provider,
    mock_model,
):
    mock_model.encode.side_effect = RuntimeError(
        "Model error"
    )

    with pytest.raises(RuntimeError):
        provider.embed(
            EmbeddingRequest(
                texts=["hello"]
            )
        )


def test_query_model_error(
    provider,
    mock_model,
):
    mock_model.encode.side_effect = RuntimeError(
        "Model error"
    )

    with pytest.raises(RuntimeError):
        provider.embed_query(
            "hello"
        )