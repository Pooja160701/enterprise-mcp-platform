import pytest

from app.tool_selection.intent_classifier import IntentClassifier
from app.tool_selection.models import IntentType


@pytest.fixture
def classifier():
    return IntentClassifier()


# -------------------------------------------------
# Classification
# -------------------------------------------------


def test_classify_search(classifier):
    result = classifier.classify("search for Python tutorials")
    assert result.intent == IntentType.SEARCH
    assert result.confidence > 0


def test_classify_code(classifier):
    result = classifier.classify("write python code")
    assert result.intent == IntentType.CODE


def test_classify_database(classifier):
    result = classifier.classify("select from sql table")
    assert result.intent == IntentType.DATABASE


def test_classify_unknown(classifier):
    result = classifier.classify("abcdefghijklmnop")
    assert result.intent == IntentType.UNKNOWN
    assert result.confidence == 0.0


def test_classify_empty_string(classifier):
    result = classifier.classify("")
    assert result.intent == IntentType.UNKNOWN
    assert result.confidence == 0.0


def test_classify_whitespace(classifier):
    result = classifier.classify("     ")
    assert result.intent == IntentType.UNKNOWN


def test_confidence_range(classifier):
    result = classifier.classify("search find lookup")
    assert 0.0 <= result.confidence <= 1.0


# -------------------------------------------------
# Multi Intent
# -------------------------------------------------


def test_multiple_intents(classifier):
    results = classifier.classify_multiple(
        "search python code"
    )

    intents = {r.intent for r in results}

    assert IntentType.SEARCH in intents
    assert IntentType.CODE in intents


def test_multiple_unknown(classifier):
    results = classifier.classify_multiple(
        "xxxxxxxx"
    )

    assert len(results) == 1
    assert results[0].intent == IntentType.UNKNOWN


def test_multiple_threshold(classifier):
    results = classifier.classify_multiple(
        "search python code",
        threshold=0.8,
    )

    assert len(results) <= 1


# -------------------------------------------------
# Entity Extraction
# -------------------------------------------------


def test_extract_entities(classifier):
    entities = classifier.extract_entities(
        "OpenAI uses Python and FastAPI"
    )

    assert "OpenAI" in entities
    assert "Python" in entities
    assert "FastAPI" in entities


def test_extract_entities_unique(classifier):
    entities = classifier.extract_entities(
        "Python Python Python"
    )

    assert entities == ["Python"]


def test_extract_entities_none(classifier):
    entities = classifier.extract_entities(
        "python fastapi sql"
    )

    assert entities == []


# -------------------------------------------------
# Pattern Management
# -------------------------------------------------


def test_add_pattern(classifier):
    classifier.add_pattern(
        IntentType.SEARCH,
        r"\bgoogle\b",
    )

    assert r"\bgoogle\b" in classifier.patterns()[
        IntentType.SEARCH
    ]


def test_remove_pattern_success(classifier):
    classifier.add_pattern(
        IntentType.SEARCH,
        r"\bgoogle\b",
    )

    assert classifier.remove_pattern(
        IntentType.SEARCH,
        r"\bgoogle\b",
    )


def test_remove_pattern_failure(classifier):
    assert (
        classifier.remove_pattern(
            IntentType.SEARCH,
            r"\bmissing\b",
        )
        is False
    )


def test_patterns_returns_copy(classifier):
    patterns = classifier.patterns()

    patterns[IntentType.SEARCH].append("abc")

    assert "abc" not in classifier.patterns()[
        IntentType.SEARCH
    ]


# -------------------------------------------------
# Statistics
# -------------------------------------------------


def test_statistics(classifier):
    classifier.classify("search python")

    stats = classifier.statistics()

    assert stats["requests"] == 1


def test_clear_statistics(classifier):
    classifier.classify("search")

    classifier.clear_statistics()

    assert classifier.statistics() == {}


# -------------------------------------------------
# Reset
# -------------------------------------------------


def test_reset(classifier):
    classifier.add_pattern(
        IntentType.SEARCH,
        r"\bgoogle\b",
    )

    classifier.classify("search")

    classifier.reset()

    assert (
        r"\bgoogle\b"
        not in classifier.patterns()[
            IntentType.SEARCH
        ]
    )

    assert classifier.statistics() == {}


# -------------------------------------------------
# Dunder Methods
# -------------------------------------------------


def test_len(classifier):
    assert len(classifier) > 0


def test_contains(classifier):
    assert IntentType.SEARCH in classifier
    assert IntentType.UNKNOWN in classifier


def test_iter(classifier):
    items = list(classifier)

    assert len(items) > 0

    intent, patterns = items[0]

    assert isinstance(intent, IntentType)
    assert isinstance(patterns, list)