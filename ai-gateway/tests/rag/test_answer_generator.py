from __future__ import annotations

import pytest

from app.rag.answer_generator import AnswerGenerator
from app.rag.citation_engine import CitationEngine
from app.rag.embeddings import Embeddings
from app.rag.models import (
    AnswerRequest,
    ChunkMetadata,
    DocumentChunk,
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
    store = VectorStore(embeddings)

    chunks = [
        DocumentChunk(
            id="chunk1",
            document_id="doc1",
            text="Python is a programming language.",
            metadata=ChunkMetadata(
                document_id="doc1",
                filename="python.txt",
                page=1,
                source="Tutorial",
            ),
        ),
        DocumentChunk(
            id="chunk2",
            document_id="doc2",
            text="Docker is used for containerization.",
            metadata=ChunkMetadata(
                document_id="doc2",
                filename="docker.txt",
                page=2,
                source="Documentation",
            ),
        ),
    ]

    store.add(chunks)

    return store


@pytest.fixture
def retrieval_engine(embeddings, vector_store):
    return RetrievalEngine(
        embeddings=embeddings,
        vector_store=vector_store,
    )


@pytest.fixture
def citation_engine():
    return CitationEngine()


@pytest.fixture
def generator(
    retrieval_engine,
    citation_engine,
):
    return AnswerGenerator(
        retrieval_engine=retrieval_engine,
        citation_engine=citation_engine,
    )


# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------


def test_generate(generator):
    response = generator.generate(
        AnswerRequest(
            question="What is Python?",
        )
    )

    assert response.answer
    assert isinstance(response.citations, list)
    assert isinstance(
        response.retrieved_chunks,
        list,
    )


def test_generate_empty():
    embeddings = Embeddings(dimensions=16)

    store = VectorStore(embeddings)

    retrieval = RetrievalEngine(
        embeddings,
        store,
    )

    generator = AnswerGenerator(
        retrieval,
        CitationEngine(),
    )

    response = generator.generate(
        AnswerRequest(
            question="Unknown question",
        )
    )

    assert (
        "could not find"
        in response.answer.lower()
    )

    assert response.citations == []
    assert response.retrieved_chunks == []


def test_generate_top_k(generator):
    response = generator.generate(
        AnswerRequest(
            question="Python",
            top_k=1,
        )
    )

    assert (
        len(response.retrieved_chunks)
        <= 1
    )


# ---------------------------------------------------------
# Context Builder
# ---------------------------------------------------------


def test_build_context(generator):
    response = generator.generate(
        AnswerRequest(
            question="Python",
        )
    )

    context = generator._build_context(
        response.retrieved_chunks
    )

    assert isinstance(context, str)
    assert len(context) > 0


def test_build_context_empty(generator):
    assert (
        generator._build_context([])
        == ""
    )


# ---------------------------------------------------------
# Mock LLM
# ---------------------------------------------------------


def test_generate_answer(generator):
    answer = generator._generate_answer(
        question="What is Python?",
        context="Python is a programming language.",
    )

    assert "Question:" in answer
    assert "Answer:" in answer
    assert "Python" in answer


def test_generate_answer_empty_context(
    generator,
):
    answer = generator._generate_answer(
        question="Hello",
        context="",
    )

    assert (
        "could not find"
        in answer.lower()
    )


def test_generate_answer_long_context(
    generator,
):
    context = "A" * 1000

    answer = generator._generate_answer(
        question="Long?",
        context=context,
    )

    assert answer.endswith("...")


# ---------------------------------------------------------
# Ask Convenience API
# ---------------------------------------------------------


def test_ask(generator):
    response = generator.ask(
        "What is Docker?"
    )

    assert response.answer


def test_ask_with_top_k(generator):
    response = generator.ask(
        "Python",
        top_k=1,
    )

    assert (
        len(response.retrieved_chunks)
        <= 1
    )


def test_ask_with_filters(generator):
    response = generator.ask(
        "Python",
        filters={
            "source": "Tutorial",
        },
    )

    for result in response.retrieved_chunks:
        assert (
            result.chunk.metadata.source
            == "Tutorial"
        )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(generator):
    generator.ask("Python")

    stats = generator.statistics()

    assert stats["requests"] == 1
    assert stats["answers"] == 1
    assert (
        stats["retrieved_chunks"]
        >= 0
    )


def test_multiple_requests(generator):
    for _ in range(5):
        generator.ask("Python")

    stats = generator.statistics()

    assert stats["requests"] == 5
    assert stats["answers"] == 5


def test_clear_statistics(generator):
    generator.ask("Python")

    generator.clear_statistics()

    assert (
        generator.statistics()
        == {}
    )


def test_reset(generator):
    generator.ask("Python")

    generator.reset()

    assert (
        generator.statistics()
        == {}
    )


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(generator):
    config = generator.configuration()

    assert (
        config["retrieval_engine"]
        == "RetrievalEngine"
    )

    assert (
        config["citation_engine"]
        == "CitationEngine"
    )

    assert (
        config["generator"]
        == "mock_llm"
    )


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(generator):
    assert len(generator) == 3


def test_iter(generator):
    config = dict(generator)

    assert (
        config["generator"]
        == "mock_llm"
    )


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode_question(generator):
    response = generator.ask(
        "தமிழ் 😀 日本語"
    )

    assert isinstance(
        response.answer,
        str,
    )


# ---------------------------------------------------------
# Large Question
# ---------------------------------------------------------


def test_large_question(generator):
    question = "Python " * 5000

    response = generator.ask(question)

    assert response.answer


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_zero_top_k(generator):
    response = generator.ask(
        "Python",
        top_k=0,
    )

    assert (
        response.retrieved_chunks
        == []
    )


def test_filters_no_match(generator):
    response = generator.ask(
        "Python",
        filters={
            "source": "Missing",
        },
    )

    assert (
        response.retrieved_chunks
        == []
    )

    assert response.answer


def test_answer_contains_context_preview(
    generator,
):
    response = generator.ask(
        "Python"
    )

    assert (
        "generated using the retrieved context"
        in response.answer
    )


def test_citations_match_results(
    generator,
):
    response = generator.ask(
        "Python"
    )

    assert (
        len(response.citations)
        == len(response.retrieved_chunks)
    )