import pytest

from app.hybrid_search.hybrid_search import HybridSearch
from app.hybrid_search.models import (
    SearchDocument,
    SearchRequest,
    SearchType,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def search():

    return HybridSearch()


@pytest.fixture
def documents():

    return [

        SearchDocument(
            id="1",
            text="Python FastAPI Docker Kubernetes",
            embedding=[1.0, 0.0, 0.0],
            metadata={
                "language": "python",
                "year": 2024,
            },
        ),

        SearchDocument(
            id="2",
            text="Python Machine Learning TensorFlow",
            embedding=[0.9, 0.1, 0.0],
            metadata={
                "language": "python",
                "year": 2023,
            },
        ),

        SearchDocument(
            id="3",
            text="Java Spring Boot",
            embedding=[0.0, 1.0, 0.0],
            metadata={
                "language": "java",
                "year": 2022,
            },
        ),

    ]


@pytest.fixture
def embedding():

    return [1.0, 0.0, 0.0]


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------


def test_hybrid_search(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python"
    )

    result = search.search(
        request,
        documents,
        embedding,
    )

    assert len(result.results) > 0


def test_search_without_embedding(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    result = search.search(
        request,
        documents,
    )

    assert len(result.results) > 0


def test_search_empty_documents(
    search,
):

    request = SearchRequest(
        query="python"
    )

    result = search.search(
        request,
        [],
    )

    assert result.results == []


def test_search_top_k(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python",
        top_k=1,
    )

    result = search.search(
        request,
        documents,
        embedding,
    )

    assert len(result.results) == 1


# ---------------------------------------------------------
# Metadata Filtering
# ---------------------------------------------------------


def test_metadata_filter(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python",
        filters={
            "year": 2024,
        },
    )

    result = search.search(
        request,
        documents,
        embedding,
    )

    assert len(result.results) == 1
    assert result.results[0].document.id == "1"


def test_metadata_filter_no_match(
    search,
    documents,
):

    request = SearchRequest(
        query="python",
        filters={
            "year": 2030,
        },
    )

    result = search.search(
        request,
        documents,
    )

    assert result.results == []


# ---------------------------------------------------------
# Best
# ---------------------------------------------------------


def test_best(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python"
    )

    best = search.best(
        request,
        documents,
        embedding,
    )

    assert best is not None


def test_best_empty(
    search,
):

    request = SearchRequest(
        query="python"
    )

    assert search.best(
        request,
        [],
    ) is None


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python"
    )

    search.search(
        request,
        documents,
        embedding,
    )

    stats = search.statistics()

    assert "keyword" in stats
    assert "bm25" in stats
    assert "vector" in stats
    assert "fusion" in stats
    assert "reranker" in stats


def test_clear_statistics(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python"
    )

    search.search(
        request,
        documents,
        embedding,
    )

    search.clear_statistics()

    stats = search.statistics()

    for value in stats.values():

        assert value == {}


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------


def test_reset(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python"
    )

    search.search(
        request,
        documents,
        embedding,
    )

    search.reset()

    stats = search.statistics()

    for value in stats.values():

        assert value == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    search,
):

    config = search.configuration()

    assert "keyword" in config
    assert "bm25" in config
    assert "vector" in config
    assert "fusion" in config
    assert "reranker" in config


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(
    search,
):

    assert len(search) == 6


def test_iter(
    search,
):

    config = dict(iter(search))

    assert "keyword" in config
    assert "bm25" in config
    assert "vector" in config


# ---------------------------------------------------------
# Search Types
# ---------------------------------------------------------


def test_keyword_only(
    search,
    documents,
):

    request = SearchRequest(
        query="docker",
        search_type=SearchType.KEYWORD,
    )

    result = search.search(
        request,
        documents,
    )

    assert len(result.results) > 0


def test_bm25_only(
    search,
    documents,
):

    request = SearchRequest(
        query="docker",
        search_type=SearchType.BM25,
    )

    result = search.search(
        request,
        documents,
    )

    assert len(result.results) > 0


def test_vector_only(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python",
        search_type=SearchType.VECTOR,
    )

    result = search.search(
        request,
        documents,
        embedding,
    )

    assert len(result.results) > 0


def test_hybrid_type(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python",
        search_type=SearchType.HYBRID,
    )

    result = search.search(
        request,
        documents,
        embedding,
    )

    assert len(result.results) > 0


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_empty_query(
    search,
    documents,
):

    request = SearchRequest(
        query=""
    )

    result = search.search(
        request,
        documents,
    )

    assert result is not None


def test_multiple_searches(
    search,
    documents,
    embedding,
):

    request = SearchRequest(
        query="python"
    )

    for _ in range(5):

        search.search(
            request,
            documents,
            embedding,
        )

    stats = search.statistics()

    assert stats["keyword"]["requests"] == 5
    assert stats["bm25"]["requests"] == 5
    assert stats["fusion"]["requests"] == 5


def test_unicode_query(
    search,
    embedding,
):

    docs = [

        SearchDocument(
            id="1",
            text="Python Café",
            embedding=[1.0, 0.0],
        )

    ]

    request = SearchRequest(
        query="café"
    )

    result = search.search(
        request,
        docs,
        [1.0, 0.0],
    )

    assert len(result.results) == 1


def test_single_document(
    search,
    embedding,
):

    docs = [

        SearchDocument(
            id="1",
            text="Python",
            embedding=[1.0, 0.0],
        )

    ]

    request = SearchRequest(
        query="python"
    )

    result = search.search(
        request,
        docs,
        [1.0, 0.0],
    )

    assert len(result.results) == 1