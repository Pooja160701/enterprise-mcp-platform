from __future__ import annotations

import pytest

from app.rag.models import (
    AnswerRequest,
    AnswerResponse,
    ChunkMetadata,
    Citation,
    CitationResult,
    Document,
    DocumentChunk,
    DocumentType,
    EmbeddingProvider,
    EmbeddingRequest,
    EmbeddingResponse,
    RetrievalRequest,
    RetrievalResult,
    VectorStoreStats,
    VectorStoreType,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def metadata():
    return ChunkMetadata(
        document_id="doc1",
        filename="sample.txt",
        document_type=DocumentType.TEXT,
        chunk_index=0,
        page=1,
        start_char=0,
        end_char=100,
        source="unit-test",
        extra={"author": "tester"},
    )


@pytest.fixture
def chunk(metadata):
    return DocumentChunk(
        id="chunk1",
        document_id="doc1",
        text="Hello World",
        metadata=metadata,
        embedding=[0.1, 0.2, 0.3],
    )


# ---------------------------------------------------------
# Enum Tests
# ---------------------------------------------------------


def test_document_type_values():
    assert DocumentType.TEXT.value == "text"
    assert DocumentType.PDF.value == "pdf"
    assert DocumentType.MARKDOWN.value == "markdown"
    assert DocumentType.UNKNOWN.value == "unknown"


def test_embedding_provider_values():
    assert EmbeddingProvider.MOCK.value == "mock"
    assert EmbeddingProvider.OPENAI.value == "openai"
    assert EmbeddingProvider.AZURE.value == "azure"
    assert (
        EmbeddingProvider.SENTENCE_TRANSFORMERS.value
        == "sentence_transformers"
    )


def test_vector_store_values():
    assert VectorStoreType.MEMORY.value == "memory"
    assert VectorStoreType.CHROMA.value == "chroma"
    assert VectorStoreType.FAISS.value == "faiss"
    assert VectorStoreType.QDRANT.value == "qdrant"
    assert VectorStoreType.PINECONE.value == "pinecone"


# ---------------------------------------------------------
# ChunkMetadata
# ---------------------------------------------------------


def test_chunk_metadata_creation(metadata):
    assert metadata.document_id == "doc1"
    assert metadata.filename == "sample.txt"
    assert metadata.page == 1
    assert metadata.extra["author"] == "tester"


def test_chunk_metadata_defaults():
    metadata = ChunkMetadata(
        document_id="doc",
        filename="file.txt",
    )

    assert metadata.document_type == DocumentType.TEXT
    assert metadata.chunk_index == 0
    assert metadata.page is None
    assert metadata.extra == {}


# ---------------------------------------------------------
# Document
# ---------------------------------------------------------


def test_document_creation():
    document = Document(
        id="1",
        filename="notes.md",
        content="markdown",
        document_type=DocumentType.MARKDOWN,
    )

    assert document.id == "1"
    assert document.filename == "notes.md"
    assert document.document_type == DocumentType.MARKDOWN


def test_document_metadata_default():
    document = Document(
        id="1",
        filename="a.txt",
        content="abc",
    )

    assert document.metadata == {}


# ---------------------------------------------------------
# DocumentChunk
# ---------------------------------------------------------


def test_document_chunk_creation(chunk):
    assert chunk.id == "chunk1"
    assert chunk.text == "Hello World"
    assert len(chunk.embedding) == 3


def test_document_chunk_default_embedding(metadata):
    chunk = DocumentChunk(
        id="id",
        document_id="doc",
        text="abc",
        metadata=metadata,
    )

    assert chunk.embedding == []


# ---------------------------------------------------------
# Embeddings
# ---------------------------------------------------------


def test_embedding_request():
    request = EmbeddingRequest(
        texts=["a", "b"],
    )

    assert request.provider == EmbeddingProvider.MOCK
    assert len(request.texts) == 2


def test_embedding_response():
    response = EmbeddingResponse(
        provider=EmbeddingProvider.OPENAI,
        dimensions=3,
        embeddings=[
            [1.0, 2.0, 3.0],
        ],
    )

    assert response.provider == EmbeddingProvider.OPENAI
    assert response.dimensions == 3


# ---------------------------------------------------------
# Retrieval
# ---------------------------------------------------------


def test_retrieval_request_defaults():
    request = RetrievalRequest(
        query="python",
    )

    assert request.top_k == 5
    assert request.filters == {}


def test_retrieval_result(chunk):
    result = RetrievalResult(
        chunk=chunk,
        score=0.95,
    )

    assert result.score == pytest.approx(0.95)
    assert result.chunk.id == "chunk1"


# ---------------------------------------------------------
# Citation
# ---------------------------------------------------------


def test_citation():
    citation = Citation(
        index=1,
        document_id="doc",
        filename="file.pdf",
        chunk_id="chunk1",
        page=10,
        source="book",
        score=0.98,
    )

    assert citation.page == 10
    assert citation.score == pytest.approx(0.98)


def test_citation_result_default():
    result = CitationResult()

    assert result.citations == []


# ---------------------------------------------------------
# Answer Generation
# ---------------------------------------------------------


def test_answer_request_defaults():
    request = AnswerRequest(
        question="What is AI?",
    )

    assert request.top_k == 5
    assert request.filters == {}


def test_answer_response_defaults():
    response = AnswerResponse(
        answer="Artificial Intelligence",
    )

    assert response.answer.startswith("Artificial")
    assert response.citations == []
    assert response.retrieved_chunks == []


# ---------------------------------------------------------
# Vector Store Stats
# ---------------------------------------------------------


def test_vector_store_stats():
    stats = VectorStoreStats(
        documents=2,
        chunks=10,
        dimensions=768,
        provider=EmbeddingProvider.OPENAI,
        store=VectorStoreType.FAISS,
    )

    assert stats.documents == 2
    assert stats.chunks == 10
    assert stats.dimensions == 768
    assert stats.provider == EmbeddingProvider.OPENAI
    assert stats.store == VectorStoreType.FAISS


def test_vector_store_stats_defaults():
    stats = VectorStoreStats()

    assert stats.documents == 0
    assert stats.chunks == 0
    assert stats.dimensions == 0
    assert stats.provider == EmbeddingProvider.MOCK
    assert stats.store == VectorStoreType.MEMORY


# ---------------------------------------------------------
# Serialization
# ---------------------------------------------------------


def test_model_dump(chunk):
    dumped = chunk.model_dump()

    assert dumped["id"] == "chunk1"
    assert dumped["document_id"] == "doc1"
    assert dumped["metadata"]["filename"] == "sample.txt"


def test_model_dump_json(chunk):
    json_data = chunk.model_dump_json()

    assert "chunk1" in json_data
    assert "Hello World" in json_data


# ---------------------------------------------------------
# Equality
# ---------------------------------------------------------


def test_models_equality(metadata):
    m1 = ChunkMetadata(
        document_id="1",
        filename="a.txt",
    )

    m2 = ChunkMetadata(
        document_id="1",
        filename="a.txt",
    )

    assert m1 == m2


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "",
        " ",
        "தமிழ்",
        "日本語",
        "😀 Emoji",
        "123456",
    ],
)
def test_embedding_request_edge_cases(text):
    request = EmbeddingRequest(
        texts=[text],
    )

    assert request.texts[0] == text


def test_large_embedding():
    embedding = [0.1] * 4096

    response = EmbeddingResponse(
        provider=EmbeddingProvider.MOCK,
        dimensions=4096,
        embeddings=[embedding],
    )

    assert len(response.embeddings[0]) == 4096


def test_nested_extra_metadata():
    metadata = ChunkMetadata(
        document_id="doc",
        filename="file",
        extra={
            "nested": {
                "a": 1,
                "b": [1, 2, 3],
            }
        },
    )

    assert metadata.extra["nested"]["a"] == 1
    assert metadata.extra["nested"]["b"] == [1, 2, 3]