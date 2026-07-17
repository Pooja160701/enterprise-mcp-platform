import math

import pytest

from app.hybrid_search.bm25_search import BM25Search
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

    return BM25Search()


@pytest.fixture
def documents():

    return [

        SearchDocument(
            id="1",
            text="python fastapi docker kubernetes",
        ),

        SearchDocument(
            id="2",
            text="python machine learning tensorflow",
        ),

        SearchDocument(
            id="3",
            text="java spring boot",
        ),

        SearchDocument(
            id="4",
            text="python python python docker",
        ),

    ]


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------


def test_search_returns_results(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    results = search.search(
        request,
        documents,
    )

    assert len(results) == 3


def test_search_empty_documents(
    search,
):

    request = SearchRequest(
        query="python"
    )

    assert search.search(
        request,
        [],
    ) == []


def test_search_no_match(
    search,
    documents,
):

    request = SearchRequest(
        query="golang"
    )

    assert search.search(
        request,
        documents,
    ) == []


def test_search_top_k(
    search,
    documents,
):

    request = SearchRequest(
        query="python",
        top_k=2,
    )

    results = search.search(
        request,
        documents,
    )

    assert len(results) == 2


def test_search_assigns_rank(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    results = search.search(
        request,
        documents,
    )

    assert results[0].rank == 1
    assert results[1].rank == 2


def test_search_source(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    results = search.search(
        request,
        documents,
    )

    for result in results:

        assert result.source == SearchType.BM25


# ---------------------------------------------------------
# Tokenization
# ---------------------------------------------------------


def test_tokenize(
    search,
):

    tokens = search._tokenize(
        "Python FastAPI Docker"
    )

    assert tokens == [
        "python",
        "fastapi",
        "docker",
    ]


def test_tokenize_empty(
    search,
):

    assert search._tokenize("") == []


# ---------------------------------------------------------
# IDF
# ---------------------------------------------------------


def test_compute_idf(
    search,
):

    corpus = [

        ["python", "docker"],

        ["python"],

        ["java"],

    ]

    idf = search._compute_idf(
        corpus
    )

    assert "python" in idf
    assert "docker" in idf
    assert "java" in idf


def test_idf_values_positive(
    search,
):

    corpus = [

        ["python"],

        ["docker"],

    ]

    idf = search._compute_idf(
        corpus
    )

    assert idf["python"] > 0
    assert idf["docker"] > 0


# ---------------------------------------------------------
# BM25 Score
# ---------------------------------------------------------


def test_bm25_score_positive(
    search,
):

    query = ["python"]

    document = [
        "python",
        "docker",
        "python",
    ]

    idf = {

        "python": 1.0,

    }

    score = search._bm25_score(
        query_terms=query,
        document=document,
        idf=idf,
        avg_doc_length=3,
    )

    assert score > 0


def test_bm25_score_no_match(
    search,
):

    score = search._bm25_score(
        query_terms=["aws"],
        document=["python"],
        idf={"aws": 1.0},
        avg_doc_length=1,
    )

    assert score == 0.0


def test_bm25_multiple_terms(
    search,
):

    score = search._bm25_score(
        query_terms=[
            "python",
            "docker",
        ],
        document=[
            "python",
            "docker",
            "docker",
        ],
        idf={
            "python": 1.0,
            "docker": 1.0,
        },
        avg_doc_length=3,
    )

    assert score > 1.0


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    search,
):

    config = search.configuration()

    assert config["algorithm"] == "bm25"
    assert config["k1"] == 1.5
    assert config["b"] == 0.75


def test_custom_configuration():

    search = BM25Search(
        k1=2.0,
        b=0.5,
    )

    config = search.configuration()

    assert config["k1"] == 2.0
    assert config["b"] == 0.5


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    search.search(
        request,
        documents,
    )

    stats = search.statistics()

    assert stats["requests"] == 1
    assert stats["matched"] == 3


def test_clear_statistics(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    search.search(
        request,
        documents,
    )

    search.clear_statistics()

    assert search.statistics() == {}


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------


def test_reset(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    search.search(
        request,
        documents,
    )

    search.reset()

    assert search.statistics() == {}

    config = search.configuration()

    assert config["k1"] == 1.5
    assert config["b"] == 0.75


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(
    search,
):

    assert len(search) == 3


def test_iter(
    search,
):

    config = dict(iter(search))

    assert config["algorithm"] == "bm25"


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_case_insensitive(
    search,
):

    docs = [

        SearchDocument(
            id="1",
            text="PYTHON FASTAPI",
        )

    ]

    request = SearchRequest(
        query="python"
    )

    results = search.search(
        request,
        docs,
    )

    assert len(results) == 1


def test_unicode_text(
    search,
):

    docs = [

        SearchDocument(
            id="1",
            text="Python Café",
        )

    ]

    request = SearchRequest(
        query="café"
    )

    results = search.search(
        request,
        docs,
    )

    assert len(results) == 1


def test_empty_document_text(
    search,
):

    docs = [

        SearchDocument(
            id="1",
            text="",
        )

    ]

    request = SearchRequest(
        query="python"
    )

    assert search.search(
        request,
        docs,
    ) == []


def test_multiple_searches(
    search,
    documents,
):

    request = SearchRequest(
        query="python"
    )

    for _ in range(5):

        search.search(
            request,
            documents,
        )

    stats = search.statistics()

    assert stats["requests"] == 5
    assert stats["matched"] == 15


def test_idf_with_single_document(
    search,
):

    corpus = [

        ["python", "docker"]

    ]

    idf = search._compute_idf(
        corpus
    )

    assert math.isfinite(
        idf["python"]
    )


def test_bm25_empty_query(
    search,
):

    score = search._bm25_score(
        query_terms=[],
        document=["python"],
        idf={},
        avg_doc_length=1,
    )

    assert score == 0.0


def test_bm25_empty_document(
    search,
):

    score = search._bm25_score(
        query_terms=["python"],
        document=[],
        idf={"python": 1.0},
        avg_doc_length=1,
    )

    assert score == 0.0


def test_custom_parameters():

    search = BM25Search(
        k1=1.8,
        b=0.6,
    )

    assert search.configuration()["k1"] == 1.8
    assert search.configuration()["b"] == 0.6