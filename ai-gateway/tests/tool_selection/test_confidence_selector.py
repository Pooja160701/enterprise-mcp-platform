import pytest

from app.tool_selection.confidence_selector import ConfidenceSelector
from app.tool_selection.models import (
    SelectionResult,
    ToolCandidate,
    ToolMetadata,
)


@pytest.fixture
def selector():
    return ConfidenceSelector()


@pytest.fixture
def candidate1():
    tool = ToolMetadata(
        name="GPT-4",
        description="",
        provider="OpenAI",
        capabilities=[],
        reliability=0.95,
        confidence=0.95,
        average_latency_ms=100,
        average_cost=0.01,
        enabled=True,
    )

    return ToolCandidate(
        tool=tool,
        total_score=0.95,
    )


@pytest.fixture
def candidate2():
    tool = ToolMetadata(
        name="Claude",
        description="",
        provider="Anthropic",
        capabilities=[],
        reliability=0.90,
        confidence=0.85,
        average_latency_ms=200,
        average_cost=0.02,
        enabled=True,
    )

    return ToolCandidate(
        tool=tool,
        total_score=0.80,
    )


@pytest.fixture
def candidate3():
    tool = ToolMetadata(
        name="Gemini",
        description="",
        provider="Google",
        capabilities=[],
        reliability=0.80,
        confidence=0.60,
        average_latency_ms=300,
        average_cost=0.03,
        enabled=True,
    )

    return ToolCandidate(
        tool=tool,
        total_score=0.40,
    )


# -------------------------------------------------
# Configuration
# -------------------------------------------------


def test_default_configuration(selector):
    assert selector.minimum_confidence == 0.70


def test_set_minimum_confidence(selector):
    selector.minimum_confidence = 0.80
    assert selector.minimum_confidence == 0.80


def test_confidence_clamped_low(selector):
    selector.minimum_confidence = -1
    assert selector.minimum_confidence == 0.0


def test_confidence_clamped_high(selector):
    selector.minimum_confidence = 5
    assert selector.minimum_confidence == 1.0


# -------------------------------------------------
# Confident
# -------------------------------------------------


def test_confident_true(selector, candidate1):
    assert selector.confident(candidate1)


def test_confident_false(selector, candidate3):
    assert not selector.confident(candidate3)


# -------------------------------------------------
# Filter
# -------------------------------------------------


def test_filter(selector, candidate1, candidate2, candidate3):
    filtered = selector.filter(
        [candidate1, candidate2, candidate3]
    )

    assert len(filtered) == 2


def test_filter_empty(selector):
    assert selector.filter([]) == []


def test_filter_statistics(selector, candidate1, candidate3):
    selector.filter([candidate1, candidate3])

    stats = selector.statistics()

    assert stats["requests"] == 1
    assert stats["accepted"] == 1
    assert stats["rejected"] == 1


# -------------------------------------------------
# Select
# -------------------------------------------------


def test_select_success(selector, candidate1, candidate2):
    result = selector.select(
        [candidate2, candidate1]
    )

    assert isinstance(result, SelectionResult)
    assert result.selected.name == "GPT-4"
    assert len(result.fallback_tools) == 1


def test_select_no_confident(selector, candidate3):
    result = selector.select([candidate3])

    assert result.selected is None
    assert len(result.fallback_tools) == 1
    assert "minimum confidence" in result.reason.lower()


def test_select_empty(selector):
    result = selector.select([])

    assert result.selected is None
    assert result.candidates == []
    assert result.fallback_tools == []


# -------------------------------------------------
# Best
# -------------------------------------------------


def test_best(selector, candidate1, candidate2):
    best = selector.best(
        [candidate2, candidate1]
    )

    assert best.tool.name == "GPT-4"


def test_best_none(selector, candidate3):
    assert selector.best([candidate3]) is None


def test_best_empty(selector):
    assert selector.best([]) is None


# -------------------------------------------------
# Fallbacks
# -------------------------------------------------


def test_fallbacks(selector, candidate1, candidate2):
    fallbacks = selector.fallbacks(
        [candidate1, candidate2]
    )

    assert len(fallbacks) == 1
    assert fallbacks[0].tool.name == "Claude"


def test_fallbacks_single(selector, candidate1):
    assert selector.fallbacks([candidate1]) == []


def test_fallbacks_none(selector, candidate3):
    assert selector.fallbacks([candidate3]) == []


# -------------------------------------------------
# Statistics
# -------------------------------------------------


def test_clear_statistics(selector, candidate1):
    selector.filter([candidate1])

    selector.clear_statistics()

    assert selector.statistics() == {}


# -------------------------------------------------
# Reset
# -------------------------------------------------


def test_reset(selector, candidate1):
    selector.minimum_confidence = 0.95

    selector.filter([candidate1])

    selector.reset()

    assert selector.minimum_confidence == 0.70
    assert selector.statistics() == {}


# -------------------------------------------------
# Utilities
# -------------------------------------------------


def test_configuration(selector):
    config = selector.configuration()

    assert config["minimum_confidence"] == 0.70


# -------------------------------------------------
# Dunder
# -------------------------------------------------


def test_len(selector):
    assert len(selector) == 1


def test_iter(selector):
    items = dict(iter(selector))

    assert "minimum_confidence" in items
    assert items["minimum_confidence"] == 0.70