from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional

from app.tool_selection.models import (
    Capability,
    IntentResult,
    IntentType,
    ToolCandidate,
    ToolMetadata,
)


class CapabilityMatcher:
    """
    Enterprise Capability Matcher

    Responsibilities
    ----------------
    • Map intents to required capabilities
    • Match tools against capabilities
    • Score capability coverage
    • Rank compatible tools
    • Maintain matching statistics
    """

    INTENT_CAPABILITIES = {
        IntentType.SEARCH: [
            Capability.SEARCH,
            Capability.WEB,
        ],
        IntentType.CALCULATE: [
            Capability.PYTHON,
        ],
        IntentType.CODE: [
            Capability.PYTHON,
            Capability.API,
        ],
        IntentType.DATABASE: [
            Capability.SQL,
        ],
        IntentType.FILESYSTEM: [
            Capability.FILESYSTEM,
        ],
        IntentType.WEB: [
            Capability.WEB,
        ],
        IntentType.EMAIL: [
            Capability.EMAIL,
        ],
        IntentType.CALENDAR: [
            Capability.CALENDAR,
        ],
        IntentType.ANALYTICS: [
            Capability.PYTHON,
            Capability.SQL,
        ],
        IntentType.CHAT: [
            Capability.REASONING,
        ],
        IntentType.UNKNOWN: [],
    }

    def __init__(self):

        self._intent_map = {
            intent: list(capabilities)
            for intent, capabilities
            in self.INTENT_CAPABILITIES.items()
        }

        self._statistics = Counter()

    # -------------------------------------------------
    # Required Capabilities
    # -------------------------------------------------

    def required_capabilities(
        self,
        intent: IntentType,
    ) -> List[Capability]:

        return list(
            self._intent_map.get(
                intent,
                [],
            )
        )

    # -------------------------------------------------
    # Match Single Tool
    # -------------------------------------------------

    def match(
        self,
        tool: ToolMetadata,
        intent: IntentResult,
    ) -> ToolCandidate:

        required = self.required_capabilities(
            intent.intent
        )

        if not required:

            score = 0.0

        else:

            matched = len(

                set(required)

                &

                set(tool.capabilities)

            )

            score = matched / len(required)

        candidate = ToolCandidate(

            tool=tool,

            capability_score=round(
                score,
                3,
            ),

        )

        self._statistics["requests"] += 1

        if score > 0:

            self._statistics["matched"] += 1

        else:

            self._statistics["unmatched"] += 1

        return candidate

    # -------------------------------------------------
    # Match All Tools
    # -------------------------------------------------

    def match_all(
        self,
        tools: List[ToolMetadata],
        intent: IntentResult,
    ) -> List[ToolCandidate]:

        candidates = [

            self.match(
                tool,
                intent,
            )

            for tool

            in tools

            if tool.enabled

        ]

        candidates.sort(

            key=lambda candidate: (

                candidate.capability_score,

                candidate.tool.reliability,

            ),

            reverse=True,

        )

        return candidates

    # -------------------------------------------------
    # Best Match
    # -------------------------------------------------

    def best_match(
        self,
        tools: List[ToolMetadata],
        intent: IntentResult,
    ) -> Optional[ToolCandidate]:

        candidates = self.match_all(

            tools,

            intent,

        )

        if not candidates:

            return None

        return candidates[0]

    # -------------------------------------------------
    # Compatibility
    # -------------------------------------------------

    def compatible(
        self,
        tool: ToolMetadata,
        intent: IntentResult,
    ) -> bool:

        return (

            self.match(

                tool,

                intent,

            ).capability_score

            > 0

        )

    # -------------------------------------------------
    # Intent Mapping
    # -------------------------------------------------

    def set_mapping(
        self,
        intent: IntentType,
        capabilities: List[Capability],
    ):

        self._intent_map[intent] = list(
            capabilities
        )

    def add_capability(
        self,
        intent: IntentType,
        capability: Capability,
    ):

        mapping = self._intent_map.setdefault(
            intent,
            [],
        )

        if capability not in mapping:

            mapping.append(
                capability
            )

    def remove_capability(
        self,
        intent: IntentType,
        capability: Capability,
    ) -> bool:

        mapping = self._intent_map.get(
            intent
        )

        if (

            mapping is None

            or capability not in mapping

        ):

            return False

        mapping.remove(
            capability
        )

        return True

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ) -> dict:

        return dict(
            self._statistics
        )

    def clear_statistics(
        self,
    ):

        self._statistics.clear()

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset(self):

        self._intent_map = {

            intent: list(capabilities)

            for intent, capabilities

            in self.INTENT_CAPABILITIES.items()

        }

        self.clear_statistics()

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    def mappings(
        self,
    ) -> Dict[
        IntentType,
        List[Capability],
    ]:

        return {

            intent: list(capabilities)

            for intent, capabilities

            in self._intent_map.items()

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(self):

        return len(
            self._intent_map
        )

    def __contains__(
        self,
        intent: IntentType,
    ):

        return intent in self._intent_map

    def __iter__(self):

        return iter(
            self._intent_map.items()
        )