from __future__ import annotations

from typing import Any, Callable, List, Optional

from app.tool_selection.capability_matcher import CapabilityMatcher
from app.tool_selection.confidence_selector import ConfidenceSelector
from app.tool_selection.cost_optimizer import CostOptimizer
from app.tool_selection.fallback_manager import FallbackManager
from app.tool_selection.intent_classifier import IntentClassifier
from app.tool_selection.models import (
    IntentResult,
    SelectionResult,
    ToolCandidate,
    ToolMetadata,
)
from app.tool_selection.tool_ranker import ToolRanker


class SelectionManager:
    """
    Enterprise AI Tool Selection Manager

    Pipeline
    --------
    1. Intent Classification
    2. Capability Matching
    3. Tool Ranking
    4. Cost Optimization
    5. Confidence Selection
    6. Automatic Fallback Execution
    """

    def __init__(
        self,
        intent_classifier: Optional[IntentClassifier] = None,
        capability_matcher: Optional[
            CapabilityMatcher
        ] = None,
        tool_ranker: Optional[
            ToolRanker
        ] = None,
        cost_optimizer: Optional[
            CostOptimizer
        ] = None,
        confidence_selector: Optional[
            ConfidenceSelector
        ] = None,
        fallback_manager: Optional[
            FallbackManager
        ] = None,
    ):

        self.intent_classifier = (
            intent_classifier
            or IntentClassifier()
        )

        self.capability_matcher = (
            capability_matcher
            or CapabilityMatcher()
        )

        self.tool_ranker = (
            tool_ranker
            or ToolRanker()
        )

        self.cost_optimizer = (
            cost_optimizer
            or CostOptimizer()
        )

        self.confidence_selector = (
            confidence_selector
            or ConfidenceSelector()
        )

        self.fallback_manager = (
            fallback_manager
            or FallbackManager()
        )

    # -------------------------------------------------
    # Intent
    # -------------------------------------------------

    def classify(
        self,
        prompt: str,
    ) -> IntentResult:

        return self.intent_classifier.classify(
            prompt
        )

    # -------------------------------------------------
    # Match
    # -------------------------------------------------

    def match(
        self,
        intent: IntentResult,
        tools: List[ToolMetadata],
    ) -> List[ToolCandidate]:

        return self.capability_matcher.match_all(
            tools,
            intent,
        )

    # -------------------------------------------------
    # Rank
    # -------------------------------------------------

    def rank(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        return self.tool_ranker.rank(
            candidates
        )

    # -------------------------------------------------
    # Optimize
    # -------------------------------------------------

    def optimize(
        self,
        candidates: List[ToolCandidate],
    ) -> List[ToolCandidate]:

        return self.cost_optimizer.optimize(
            candidates
        )

    # -------------------------------------------------
    # Select
    # -------------------------------------------------

    def select(
        self,
        candidates: List[ToolCandidate],
    ) -> SelectionResult:

        return self.confidence_selector.select(
            candidates
        )

    # -------------------------------------------------
    # Complete Pipeline
    # -------------------------------------------------

    def pipeline(
        self,
        prompt: str,
        tools: List[ToolMetadata],
    ) -> SelectionResult:

        intent = self.classify(
            prompt
        )

        candidates = self.match(
            intent,
            tools,
        )

        candidates = self.rank(
            candidates
        )

        candidates = self.optimize(
            candidates
        )

        return self.select(
            candidates
        )

    # -------------------------------------------------
    # Execute
    # -------------------------------------------------

    def execute(
        self,
        prompt: str,
        tools: List[ToolMetadata],
        executor: Callable[
            [ToolCandidate],
            Any,
        ],
    ) -> Any:

        result = self.pipeline(
            prompt,
            tools,
        )

        if not result.candidates:

            raise RuntimeError(
                "No candidate tools found."
            )

        return self.fallback_manager.execute(
            result.candidates,
            executor,
        )

    # -------------------------------------------------
    # Best Tool
    # -------------------------------------------------

    def best_tool(
        self,
        prompt: str,
        tools: List[ToolMetadata],
    ) -> Optional[ToolMetadata]:

        result = self.pipeline(
            prompt,
            tools,
        )

        return result.selected

    # -------------------------------------------------
    # Top N
    # -------------------------------------------------

    def top_tools(
        self,
        prompt: str,
        tools: List[ToolMetadata],
        limit: int = 5,
    ) -> List[ToolMetadata]:

        result = self.pipeline(
            prompt,
            tools,
        )

        return [

            candidate.tool

            for candidate

            in result.candidates[:limit]

        ]

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ) -> dict:

        return {

            "intent_classifier":
                self.intent_classifier.statistics(),

            "capability_matcher":
                self.capability_matcher.statistics(),

            "tool_ranker":
                self.tool_ranker.statistics(),

            "cost_optimizer":
                self.cost_optimizer.statistics(),

            "confidence_selector":
                self.confidence_selector.statistics(),

            "fallback_manager":
                self.fallback_manager.statistics(),

        }

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset(
        self,
    ):

        self.intent_classifier.reset()

        self.capability_matcher.reset()

        self.tool_ranker.reset()

        self.cost_optimizer.reset()

        self.confidence_selector.reset()

        self.fallback_manager.reset()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "minimum_confidence":
                self.confidence_selector.minimum_confidence,

            "maximum_cost":
                self.cost_optimizer.maximum_cost,

            "preferred_provider":
                self.cost_optimizer.preferred_provider,

            "maximum_latency":
                self.cost_optimizer.maximum_latency,

            "max_retries":
                self.fallback_manager.max_retries,

            "retry_delay":
                self.fallback_manager.retry_delay,

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return 6

    def __iter__(
        self,
    ):

        yield (
            "intent_classifier",
            self.intent_classifier,
        )

        yield (
            "capability_matcher",
            self.capability_matcher,
        )

        yield (
            "tool_ranker",
            self.tool_ranker,
        )

        yield (
            "cost_optimizer",
            self.cost_optimizer,
        )

        yield (
            "confidence_selector",
            self.confidence_selector,
        )

        yield (
            "fallback_manager",
            self.fallback_manager,
        )