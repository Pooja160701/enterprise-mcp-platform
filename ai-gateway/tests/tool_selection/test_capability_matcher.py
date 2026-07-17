import pytest

from app.tool_selection.capability_matcher import CapabilityMatcher
from app.tool_selection.models import (
    Capability,
    IntentResult,
    IntentType,
    ToolMetadata,
)


@pytest.fixture
def matcher():
    return CapabilityMatcher()


@pytest.fixture
def search_intent():
    return IntentResult(
        intent=IntentType.SEARCH,
        confidence=1.0,
    )


@pytest.fixture
def tool():
    return ToolMetadata(
        name="SearchTool",
        description="Search",
        provider="OpenAI",
        capabilities=[
            Capability.SEARCH,
            Capability.WEB,
        ],
        reliability=0.95,
        enabled=True,
    )


@pytest.fixture
def sql_tool():
    return ToolMetadata(
        name="SQLTool",
        description="Database",
        provider="OpenAI",
        capabilities=[
            Capability.SQL,
        ],
        reliability=0.80,
        enabled=True,
    )


# -------------------------------------------------
# Required Capabilities
# -------------------------------------------------


def test_required_capabilities(
    matcher,
):
    caps = matcher.required_capabilities(
        IntentType.SEARCH
    )

    assert Capability.SEARCH in caps
    assert Capability.WEB in caps


def test_required_unknown(
    matcher,
):
    caps = matcher.required_capabilities(
        IntentType.UNKNOWN
    )

    assert caps == []


# -------------------------------------------------
# Match
# -------------------------------------------------


def test_match_success(
    matcher,
    tool,
    search_intent,
):
    candidate = matcher.match(
        tool,
        search_intent,
    )

    assert candidate.capability_score == 1.0


def test_match_partial(
    matcher,
    search_intent,
):
    tool = ToolMetadata(
        name="Partial",
        description="",
        provider="OpenAI",
        capabilities=[
            Capability.SEARCH,
        ],
        reliability=1.0,
        enabled=True,
    )

    candidate = matcher.match(
        tool,
        search_intent,
    )

    assert candidate.capability_score == 0.5


def test_match_failure(
    matcher,
    sql_tool,
    search_intent,
):
    candidate = matcher.match(
        sql_tool,
        search_intent,
    )

    assert candidate.capability_score == 0.0


def test_match_unknown_intent(
    matcher,
    tool,
):
    intent = IntentResult(
        intent=IntentType.UNKNOWN,
        confidence=0.0,
    )

    candidate = matcher.match(
        tool,
        intent,
    )

    assert candidate.capability_score == 0.0


# -------------------------------------------------
# Match All
# -------------------------------------------------


def test_match_all(
    matcher,
    tool,
    sql_tool,
    search_intent,
):
    candidates = matcher.match_all(
        [tool, sql_tool],
        search_intent,
    )

    assert len(candidates) == 2

    assert (
        candidates[0].tool.name
        == "SearchTool"
    )


def test_match_all_empty(
    matcher,
    search_intent,
):
    assert (
        matcher.match_all(
            [],
            search_intent,
        )
        == []
    )


def test_disabled_tool_not_returned(
    matcher,
    search_intent,
):
    tool = ToolMetadata(
        name="Disabled",
        description="",
        provider="OpenAI",
        capabilities=[
            Capability.SEARCH,
        ],
        reliability=1.0,
        enabled=False,
    )

    assert (
        matcher.match_all(
            [tool],
            search_intent,
        )
        == []
    )


# -------------------------------------------------
# Best Match
# -------------------------------------------------


def test_best_match(
    matcher,
    tool,
    sql_tool,
    search_intent,
):
    candidate = matcher.best_match(
        [tool, sql_tool],
        search_intent,
    )

    assert candidate.tool.name == "SearchTool"


def test_best_match_none(
    matcher,
    search_intent,
):
    assert (
        matcher.best_match(
            [],
            search_intent,
        )
        is None
    )


# -------------------------------------------------
# Compatible
# -------------------------------------------------


def test_compatible_true(
    matcher,
    tool,
    search_intent,
):
    assert matcher.compatible(
        tool,
        search_intent,
    )


def test_compatible_false(
    matcher,
    sql_tool,
    search_intent,
):
    assert (
        matcher.compatible(
            sql_tool,
            search_intent,
        )
        is False
    )


# -------------------------------------------------
# Mapping Management
# -------------------------------------------------


def test_set_mapping(
    matcher,
):
    matcher.set_mapping(
        IntentType.SEARCH,
        [Capability.SQL],
    )

    assert (
        matcher.required_capabilities(
            IntentType.SEARCH
        )
        == [Capability.SQL]
    )


def test_add_capability(
    matcher,
):
    matcher.add_capability(
        IntentType.SEARCH,
        Capability.SQL,
    )

    assert (
        Capability.SQL
        in matcher.required_capabilities(
            IntentType.SEARCH
        )
    )


def test_add_duplicate_capability(
    matcher,
):
    before = len(
        matcher.required_capabilities(
            IntentType.SEARCH
        )
    )

    matcher.add_capability(
        IntentType.SEARCH,
        Capability.SEARCH,
    )

    after = len(
        matcher.required_capabilities(
            IntentType.SEARCH
        )
    )

    assert before == after


def test_remove_capability(
    matcher,
):
    matcher.add_capability(
        IntentType.SEARCH,
        Capability.SQL,
    )

    assert matcher.remove_capability(
        IntentType.SEARCH,
        Capability.SQL,
    )


def test_remove_missing_capability(
    matcher,
):
    assert (
        matcher.remove_capability(
            IntentType.SEARCH,
            Capability.EMAIL,
        )
        is False
    )


# -------------------------------------------------
# Statistics
# -------------------------------------------------


def test_statistics(
    matcher,
    tool,
    search_intent,
):
    matcher.match(
        tool,
        search_intent,
    )

    stats = matcher.statistics()

    assert stats["requests"] == 1


def test_clear_statistics(
    matcher,
    tool,
    search_intent,
):
    matcher.match(
        tool,
        search_intent,
    )

    matcher.clear_statistics()

    assert matcher.statistics() == {}


# -------------------------------------------------
# Reset
# -------------------------------------------------


def test_reset(
    matcher,
):
    matcher.set_mapping(
        IntentType.SEARCH,
        [Capability.SQL],
    )

    matcher.reset()

    caps = matcher.required_capabilities(
        IntentType.SEARCH
    )

    assert Capability.WEB in caps
    assert Capability.SEARCH in caps


# -------------------------------------------------
# Dunder
# -------------------------------------------------


def test_len(
    matcher,
):
    assert len(matcher) > 0


def test_contains(
    matcher,
):
    assert IntentType.SEARCH in matcher


def test_iter(
    matcher,
):
    items = list(matcher)

    assert len(items) > 0

    intent, caps = items[0]

    assert isinstance(
        intent,
        IntentType,
    )

    assert isinstance(
        caps,
        list,
    )