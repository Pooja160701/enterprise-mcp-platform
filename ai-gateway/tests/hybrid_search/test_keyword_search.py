import pytest

from app.hybrid_search.keyword_search import KeywordSearch
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

    return KeywordSearch()


@pytest.fixture
def documents():

    return [

        SearchDocument(
            id="1",
            text="Python FastAPI Docker Kubernetes",
        ),

        SearchDocument(
            id="2",
            text="Machine Learning using Python",
        ),

        SearchDocument(
            id="3",
            text="Java Spring Boot",
        ),

        SearchDocument(
            id="4",
            text="Python Python Python",
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

    results = search.search(
        request,
        [],
    )

    assert results == []


def test_search_no_match(
    search,
    documents,
):

    request = SearchRequest(
        query="golang"
    )

    results = search.search(
        request,
        documents,
    )

    assert results == []


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


def test_search_source_type(
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

        assert result.source == SearchType.KEYWORD


# ---------------------------------------------------------
# Scoring
# ---------------------------------------------------------


def test_score_counts_occurrences(
    search,
):

    score = search._score(
        ["python"],
        "python python docker",
    )

    assert score == 2.0


def test_score_multiple_terms(
    search,
):

    score = search._score(
        ["python", "docker"],
        "python docker docker",
    )

    assert score == 3.0


def test_score_no_match(
    search,
):

    score = search._score(
        ["aws"],
        "python docker",
    )

    assert score == 0.0


def test_score_empty_text(
    search,
):

    score = search._score(
        ["python"],
        "",
    )

    assert score == 0.0


# ---------------------------------------------------------
# Tokenization
# ---------------------------------------------------------


def test_tokenize_lowercase(
    search,
):

    tokens = search._tokenize(
        "Python FASTAPI Docker"
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


def test_tokenize_multiple_spaces(
    search,
):

    tokens = search._tokenize(
        "python     docker"
    )

    assert tokens == [
        "python",
        "docker",
    ]


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


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    search,
):

    config = search.configuration()

    assert config["algorithm"] == "keyword"


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(
    search,
):

    assert len(search) == 1


def test_iter(
    search,
):

    config = dict(iter(search))

    assert config["algorithm"] == "keyword"


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_case_insensitive(
    search,
):

    documents = [

        SearchDocument(
            id="1",
            text="PYTHON FastAPI",
        )

    ]

    request = SearchRequest(
        query="python"
    )

    results = search.search(
        request,
        documents,
    )

    assert len(results) == 1


def test_repeated_query_terms(
    search,
):

    score = search._score(
        ["python", "python"],
        "python docker",
    )

    assert score == 2.0


def test_unicode_text(
    search,
):

    documents = [

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
        documents,
    )

    assert len(results) == 1


def test_document_with_empty_text(
    search,
):

    documents = [

        SearchDocument(
            id="1",
            text="",
        )

    ]

    request = SearchRequest(
        query="python"
    )

    results = search.search(
        request,
        documents,
    )

    assert results == []


def test_multiple_search_calls(
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