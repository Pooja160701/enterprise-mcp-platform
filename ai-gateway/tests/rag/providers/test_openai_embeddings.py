from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.rag.models import (
    EmbeddingProvider,
    EmbeddingRequest,
)
from app.rag.providers.openai_embeddings import (
    OpenAIEmbeddings,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_client():
    with patch(
        "app.rag.providers.openai_embeddings.OpenAI"
    ) as client_cls:
        client = MagicMock()
        client_cls.return_value = client
        yield client


@pytest.fixture
def provider(mock_client):
    return OpenAIEmbeddings(
        api_key="fake-api-key",
        model="text-embedding-3-small",
    )


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def fake_response(vectors):
    return SimpleNamespace(
        data=[
            SimpleNamespace(embedding=v)
            for v in vectors
        ]
    )


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------


def test_initialization(provider):
    assert provider.model == "text-embedding-3-small"


def test_custom_model(mock_client):
    model = OpenAIEmbeddings(
        api_key="key",
        model="text-embedding-3-large",
    )

    assert model.model == "text-embedding-3-large"


# ---------------------------------------------------------
# Embed
# ---------------------------------------------------------


def test_embed(provider, mock_client):
    mock_client.embeddings.create.return_value = (
        fake_response(
            [
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6],
            ]
        )
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
        == EmbeddingProvider.OPENAI
    )

    assert response.dimensions == 3
    assert len(response.embeddings) == 2


def test_embed_empty_request(
    provider,
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([])
    )

    response = provider.embed(
        EmbeddingRequest(
            texts=[]
        )
    )

    assert response.embeddings == []
    assert response.dimensions == 0


def test_embed_calls_sdk(
    provider,
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([[1.0]])
    )

    provider.embed(
        EmbeddingRequest(
            texts=["hello"]
        )
    )

    mock_client.embeddings.create.assert_called_once_with(
        model="text-embedding-3-small",
        input=["hello"],
    )


# ---------------------------------------------------------
# Query Embedding
# ---------------------------------------------------------


def test_embed_query(
    provider,
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response(
            [[1.0, 2.0, 3.0]]
        )
    )

    vector = provider.embed_query(
        "hello"
    )

    assert vector == [1.0, 2.0, 3.0]


def test_embed_query_calls_sdk(
    provider,
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([[0.5]])
    )

    provider.embed_query("question")

    mock_client.embeddings.create.assert_called_once_with(
        model="text-embedding-3-small",
        input="question",
    )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    provider,
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([[1.0]])
    )

    provider.embed(
        EmbeddingRequest(
            texts=["a", "b"]
        )
    )

    provider.embed_query("query")

    stats = provider.statistics()

    assert stats["requests"] == 1
    assert stats["texts"] == 2
    assert stats["queries"] == 1


def test_multiple_requests(
    provider,
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([[1.0]])
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
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([[1.0]])
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
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([[1.0]])
    )

    provider.embed_query("hello")

    provider.reset()

    assert provider.statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(provider):
    config = provider.configuration()

    assert config["provider"] == "openai"
    assert (
        config["model"]
        == "text-embedding-3-small"
    )


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(provider):
    assert len(provider) == 2


def test_iter(provider):
    config = dict(provider)

    assert config["provider"] == "openai"
    assert (
        config["model"]
        == "text-embedding-3-small"
    )


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode_query(
    provider,
    mock_client,
):
    mock_client.embeddings.create.return_value = (
        fake_response([[0.1]])
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
    mock_client,
):
    texts = [
        f"text {i}"
        for i in range(100)
    ]

    vectors = [
        [float(i)]
        for i in range(100)
    ]

    mock_client.embeddings.create.return_value = (
        fake_response(vectors)
    )

    response = provider.embed(
        EmbeddingRequest(
            texts=texts
        )
    )

    assert len(response.embeddings) == 100


# ---------------------------------------------------------
# API Errors
# ---------------------------------------------------------


def test_embed_api_error(
    provider,
    mock_client,
):
    mock_client.embeddings.create.side_effect = (
        RuntimeError("API Error")
    )

    with pytest.raises(RuntimeError):
        provider.embed(
            EmbeddingRequest(
                texts=["hello"]
            )
        )


def test_query_api_error(
    provider,
    mock_client,
):
    mock_client.embeddings.create.side_effect = (
        RuntimeError("API Error")
    )

    with pytest.raises(RuntimeError):
        provider.embed_query(
            "hello"
        )