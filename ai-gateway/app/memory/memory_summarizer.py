from collections import Counter
from copy import deepcopy


class MemorySummarizer:
    """
    Enterprise Memory Summarizer

    Produces structured summaries from conversation
    history without requiring an LLM.

    Extracts

    ✓ Facts
    ✓ Preferences
    ✓ Decisions
    ✓ Tasks
    ✓ Questions
    ✓ Important Messages
    ✓ Conversation Statistics
    """

    FACT_PREFIXES = (
        "my ",
        "i am ",
        "i'm ",
        "i have ",
        "i work",
        "i use",
        "i live",
    )

    PREFERENCE_WORDS = (
        "prefer",
        "favorite",
        "always",
        "usually",
        "never",
        "like",
        "love",
        "hate",
    )

    TASK_WORDS = (
        "todo",
        "task",
        "implement",
        "create",
        "build",
        "fix",
        "complete",
        "finish",
    )

    DECISION_WORDS = (
        "decided",
        "decision",
        "chosen",
        "selected",
        "final",
        "approved",
    )

    # ------------------------------------------------
    # Main
    # ------------------------------------------------

    @classmethod
    def summarize(
        cls,
        history,
    ):

        history = deepcopy(history)

        return {

            "facts": cls.extract_facts(history),

            "preferences": cls.extract_preferences(history),

            "decisions": cls.extract_decisions(history),

            "tasks": cls.extract_tasks(history),

            "questions": cls.extract_questions(history),

            "important_messages": cls.important(history),

            "statistics": cls.statistics(history),

        }

    # ------------------------------------------------
    # Facts
    # ------------------------------------------------

    @classmethod
    def extract_facts(
        cls,
        history,
    ):

        facts = []

        for msg in history:

            if msg.get("role") != "user":
                continue

            text = msg.get(
                "content",
                "",
            )

            lower = text.lower()

            if lower.startswith(cls.FACT_PREFIXES):

                facts.append(text)

        return facts

    # ------------------------------------------------
    # Preferences
    # ------------------------------------------------

    @classmethod
    def extract_preferences(
        cls,
        history,
    ):

        prefs = []

        for msg in history:

            text = msg.get(
                "content",
                "",
            )

            lower = text.lower()

            if any(

                word in lower

                for word in cls.PREFERENCE_WORDS

            ):

                prefs.append(text)

        return prefs

    # ------------------------------------------------
    # Decisions
    # ------------------------------------------------

    @classmethod
    def extract_decisions(
        cls,
        history,
    ):

        decisions = []

        for msg in history:

            text = msg.get(
                "content",
                "",
            )

            lower = text.lower()

            if any(

                word in lower

                for word in cls.DECISION_WORDS

            ):

                decisions.append(text)

        return decisions

    # ------------------------------------------------
    # Tasks
    # ------------------------------------------------

    @classmethod
    def extract_tasks(
        cls,
        history,
    ):

        tasks = []

        for msg in history:

            text = msg.get(
                "content",
                "",
            )

            lower = text.lower()

            if any(

                word in lower

                for word in cls.TASK_WORDS

            ):

                tasks.append(text)

        return tasks

    # ------------------------------------------------
    # Questions
    # ------------------------------------------------

    @staticmethod
    def extract_questions(
        history,
    ):

        questions = []

        for msg in history:

            text = msg.get(
                "content",
                "",
            )

            if "?" in text:

                questions.append(text)

        return questions

    # ------------------------------------------------
    # Important Messages
    # ------------------------------------------------

    @staticmethod
    def important(
        history,
        limit=10,
    ):

        ranked = sorted(

            history,

            key=lambda x: x.get(
                "importance",
                50,
            ),

            reverse=True,

        )

        return ranked[:limit]

    # ------------------------------------------------
    # Statistics
    # ------------------------------------------------

    @staticmethod
    def statistics(
        history,
    ):

        roles = Counter(

            msg.get(
                "role",
                "unknown",
            )

            for msg in history

        )

        characters = sum(

            len(

                msg.get(
                    "content",
                    "",
                )

            )

            for msg in history

        )

        words = sum(

            len(

                msg.get(
                    "content",
                    "",
                ).split()

            )

            for msg in history

        )

        return {

            "messages": len(history),

            "characters": characters,

            "words": words,

            "estimated_tokens": characters // 4,

            "roles": dict(roles),

        }

    # ------------------------------------------------
    # One-line Summary
    # ------------------------------------------------

    @classmethod
    def brief(
        cls,
        history,
    ):

        summary = cls.summarize(
            history,
        )

        return (

            f"{summary['statistics']['messages']} messages | "

            f"{len(summary['facts'])} facts | "

            f"{len(summary['preferences'])} preferences | "

            f"{len(summary['tasks'])} tasks | "

            f"{len(summary['decisions'])} decisions"

        )