from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List, Optional

from app.tool_selection.models import (
    IntentResult,
    IntentType,
)


class IntentClassifier:
    """
    Enterprise Intent Classifier

    Responsibilities
    ----------------
    • Intent classification
    • Multi-intent detection
    • Confidence estimation
    • Entity extraction
    • Statistics collection
    """

    DEFAULT_PATTERNS: Dict[IntentType, List[str]] = {
        IntentType.SEARCH: [
            r"\bsearch\b",
            r"\bfind\b",
            r"\blookup\b",
            r"\bwhere\b",
            r"\bwho\b",
            r"\bwhat\b",
        ],
        IntentType.CALCULATE: [
            r"\bcalculate\b",
            r"\bcompute\b",
            r"\bsolve\b",
            r"\bmath\b",
            r"\badd\b",
            r"\bsubtract\b",
            r"\bmultiply\b",
            r"\bdivide\b",
            r"\bpercentage\b",
        ],
        IntentType.CODE: [
            r"\bpython\b",
            r"\bcode\b",
            r"\bprogram\b",
            r"\bscript\b",
            r"\bfunction\b",
            r"\bclass\b",
            r"\bbug\b",
            r"\bdebug\b",
            r"\bapi\b",
        ],
        IntentType.DATABASE: [
            r"\bsql\b",
            r"\bdatabase\b",
            r"\btable\b",
            r"\bquery\b",
            r"\bselect\b",
            r"\binsert\b",
            r"\bupdate\b",
        ],
        IntentType.FILESYSTEM: [
            r"\bfile\b",
            r"\bfolder\b",
            r"\bdirectory\b",
            r"\bread\b",
            r"\bwrite\b",
            r"\bdelete\b",
            r"\bmove\b",
            r"\bcopy\b",
        ],
        IntentType.WEB: [
            r"\bwebsite\b",
            r"\burl\b",
            r"\bweb\b",
            r"\bbrowse\b",
            r"\binternet\b",
            r"\bonline\b",
        ],
        IntentType.EMAIL: [
            r"\bemail\b",
            r"\bmail\b",
            r"\bsend\b",
            r"\binbox\b",
        ],
        IntentType.CALENDAR: [
            r"\bcalendar\b",
            r"\bmeeting\b",
            r"\bschedule\b",
            r"\bevent\b",
            r"\bappointment\b",
        ],
        IntentType.ANALYTICS: [
            r"\banalyze\b",
            r"\banalysis\b",
            r"\breport\b",
            r"\bdashboard\b",
            r"\bstatistics\b",
            r"\bmetrics\b",
        ],
        IntentType.CHAT: [
            r"\bhello\b",
            r"\bhi\b",
            r"\bhey\b",
            r"\bthanks\b",
        ],
    }

    ENTITY_PATTERN = re.compile(
        r"\b[A-Z][a-zA-Z0-9_-]+\b"
    )

    def __init__(self):

        self._patterns = {
            intent: list(patterns)
            for intent, patterns
            in self.DEFAULT_PATTERNS.items()
        }

        self._statistics = Counter()

    # -------------------------------------------------
    # Classification
    # -------------------------------------------------

    def classify(
        self,
        text: str,
    ) -> IntentResult:

        if not text.strip():

            return IntentResult(
                intent=IntentType.UNKNOWN,
                confidence=0.0,
            )

        text_lower = text.lower()

        scores: Dict[
            IntentType,
            int,
        ] = {}

        for intent, patterns in self._patterns.items():

            score = 0

            for pattern in patterns:

                score += len(
                    re.findall(
                        pattern,
                        text_lower,
                    )
                )

            if score:

                scores[intent] = score

        if not scores:

            result = IntentResult(
                intent=IntentType.UNKNOWN,
                confidence=0.0,
                entities=self.extract_entities(
                    text
                ),
            )

            self._statistics[
                "unknown"
            ] += 1

            self._statistics[
                "requests"
            ] += 1

            return result

        best_intent = max(
            scores,
            key=scores.get,
        )

        total = sum(scores.values())

        confidence = (
            scores[best_intent]
            / total
        )

        result = IntentResult(
            intent=best_intent,
            confidence=round(
                confidence,
                3,
            ),
            entities=self.extract_entities(
                text
            ),
        )

        self._statistics[
            "requests"
        ] += 1

        self._statistics[
            best_intent.value
        ] += 1

        return result

    # -------------------------------------------------
    # Multiple Intent Detection
    # -------------------------------------------------

    def classify_multiple(
        self,
        text: str,
        threshold: float = 0.2,
    ) -> List[IntentResult]:

        text_lower = text.lower()

        scores = {}

        for intent, patterns in self._patterns.items():

            score = 0

            for pattern in patterns:

                score += len(
                    re.findall(
                        pattern,
                        text_lower,
                    )
                )

            if score:

                scores[intent] = score

        if not scores:

            return [
                IntentResult(
                    intent=IntentType.UNKNOWN,
                    confidence=0.0,
                )
            ]

        total = sum(scores.values())

        results = []

        for intent, score in sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        ):

            confidence = score / total

            if confidence >= threshold:

                results.append(
                    IntentResult(
                        intent=intent,
                        confidence=round(
                            confidence,
                            3,
                        ),
                        entities=self.extract_entities(
                            text
                        ),
                    )
                )

        return results

    # -------------------------------------------------
    # Entity Extraction
    # -------------------------------------------------

    def extract_entities(
        self,
        text: str,
    ) -> List[str]:

        entities = re.findall(
            self.ENTITY_PATTERN,
            text,
        )

        return sorted(
            set(entities)
        )

    # -------------------------------------------------
    # Pattern Management
    # -------------------------------------------------

    def add_pattern(
        self,
        intent: IntentType,
        pattern: str,
    ):

        self._patterns.setdefault(
            intent,
            [],
        ).append(pattern)

    def remove_pattern(
        self,
        intent: IntentType,
        pattern: str,
    ) -> bool:

        patterns = self._patterns.get(
            intent
        )

        if (
            patterns is None
            or pattern not in patterns
        ):

            return False

        patterns.remove(pattern)

        return True

    def patterns(
        self,
    ) -> Dict[
        IntentType,
        List[str],
    ]:

        return {
            intent: list(patterns)
            for intent, patterns
            in self._patterns.items()
        }

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
    # Utilities
    # -------------------------------------------------

    def reset(self):

        self._patterns = {
            intent: list(patterns)
            for intent, patterns
            in self.DEFAULT_PATTERNS.items()
        }

        self.clear_statistics()

    # -------------------------------------------------
    # Dunder Methods
    # -------------------------------------------------

    def __len__(self):

        return sum(
            len(patterns)
            for patterns
            in self._patterns.values()
        )

    def __contains__(
        self,
        intent: IntentType,
    ):

        return intent in self._patterns

    def __iter__(self):

        return iter(
            self._patterns.items()
        )