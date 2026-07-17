import pytest

from app.hybrid_search.metadata_filter import MetadataFilter
from app.hybrid_search.models import SearchDocument


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def metadata_filter():

    return MetadataFilter()


@pytest.fixture
def documents():

    return [

        SearchDocument(
            id="1",
            text="Python Guide",
            metadata={
                "language": "python",
                "year": 2024,
                "tags": ["ai", "ml"],
                "author": "Alice",
            },
        ),

        SearchDocument(
            id="2",
            text="Docker Handbook",
            metadata={
                "language": "docker",
                "year": 2022,
                "tags": ["devops"],
                "author": "Bob",
            },
        ),

        SearchDocument(
            id="3",
            text="Kubernetes",
            metadata={
                "language": "python",
                "year": 2023,
                "tags": ["cloud", "devops"],
                "author": "Charlie",
            },
        ),

    ]


# ---------------------------------------------------------
# Filter
# ---------------------------------------------------------


def test_filter_empty_filter(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {},
    )

    assert len(results) == 3


def test_filter_exact_match(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "language": "python",
        },
    )

    assert len(results) == 2


def test_filter_no_match(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "language": "java",
        },
    )

    assert results == []


def test_filter_multiple_conditions(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "language": "python",
            "year": 2024,
        },
    )

    assert len(results) == 1
    assert results[0].id == "1"


# ---------------------------------------------------------
# List Matching
# ---------------------------------------------------------


def test_list_contains(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "tags": "ml",
        },
    )

    assert len(results) == 1
    assert results[0].id == "1"


def test_list_no_match(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "tags": "security",
        },
    )

    assert results == []


# ---------------------------------------------------------
# Numeric Operators
# ---------------------------------------------------------


def test_gt_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "year": {
                "$gt": 2022,
            }
        },
    )

    assert len(results) == 2


def test_gte_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "year": {
                "$gte": 2023,
            }
        },
    )

    assert len(results) == 2


def test_lt_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "year": {
                "$lt": 2023,
            }
        },
    )

    assert len(results) == 1
    assert results[0].id == "2"


def test_lte_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "year": {
                "$lte": 2023,
            }
        },
    )

    assert len(results) == 2


def test_eq_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "year": {
                "$eq": 2024,
            }
        },
    )

    assert len(results) == 1


def test_ne_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "year": {
                "$ne": 2024,
            }
        },
    )

    assert len(results) == 2


def test_in_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "language": {
                "$in": [
                    "python",
                    "docker",
                ]
            }
        },
    )

    assert len(results) == 3


def test_nin_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "language": {
                "$nin": [
                    "docker",
                ]
            }
        },
    )

    assert len(results) == 2


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    metadata_filter,
    documents,
):

    metadata_filter.filter(
        documents,
        {
            "language": "python",
        },
    )

    stats = metadata_filter.statistics()

    assert stats["requests"] == 1
    assert stats["matched"] == 2


def test_clear_statistics(
    metadata_filter,
    documents,
):

    metadata_filter.filter(
        documents,
        {
            "language": "python",
        },
    )

    metadata_filter.clear_statistics()

    assert metadata_filter.statistics() == {}


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------


def test_reset(
    metadata_filter,
    documents,
):

    metadata_filter.filter(
        documents,
        {
            "language": "python",
        },
    )

    metadata_filter.reset()

    assert metadata_filter.statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    metadata_filter,
):

    config = metadata_filter.configuration()

    assert config["algorithm"] == "metadata_filter"


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(
    metadata_filter,
):

    assert len(metadata_filter) == 8


def test_iter(
    metadata_filter,
):

    config = dict(iter(metadata_filter))

    assert config["algorithm"] == "metadata_filter"


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_missing_metadata_key(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "publisher": "OReilly",
        },
    )

    assert results == []


def test_unknown_operator(
    metadata_filter,
    documents,
):

    results = metadata_filter.filter(
        documents,
        {
            "year": {
                "$unknown": 2024,
            }
        },
    )

    assert results == []


def test_empty_documents(
    metadata_filter,
):

    results = metadata_filter.filter(
        [],
        {
            "language": "python",
        },
    )

    assert results == []


def test_multiple_filter_calls(
    metadata_filter,
    documents,
):

    for _ in range(5):

        metadata_filter.filter(
            documents,
            {
                "language": "python",
            },
        )

    stats = metadata_filter.statistics()

    assert stats["requests"] == 5
    assert stats["matched"] == 10


def test_nested_metadata(
    metadata_filter,
):

    docs = [

        SearchDocument(
            id="1",
            text="Nested",
            metadata={
                "owner": {
                    "team": "AI",
                }
            },
        )

    ]

    results = metadata_filter.filter(
        docs,
        {
            "owner": {
                "team": "AI",
            }
        },
    )

    assert len(results) == 1


def test_none_metadata_value(
    metadata_filter,
):

    docs = [

        SearchDocument(
            id="1",
            text="Example",
            metadata={
                "language": None,
            },
        )

    ]

    results = metadata_filter.filter(
        docs,
        {
            "language": None,
        },
    )

    assert len(results) == 1