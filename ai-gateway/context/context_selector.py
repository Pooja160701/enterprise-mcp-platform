from copy import deepcopy


class ContextSelector:
    """
    Enterprise Context Selector

    Filters the context built by ContextBuilder
    into the most useful information for the LLM.

    Selection Order

    ✓ Session Memory
    ✓ Recent Conversation
    ✓ Long-Term Memory
    ✓ Semantic Memory

    Later phases can replace this with
    AI-based relevance scoring.
    """

    DEFAULT_LIMITS = {

        "conversation": 10,

        "long_term": 5,

        "semantic": 5,

    }

    # -------------------------------------------------
    # Select Context
    # -------------------------------------------------

    @classmethod
    def select(
        cls,
        context,
        limits=None,
    ):

        limits = {

            **cls.DEFAULT_LIMITS,

            **(limits or {}),

        }

        return {

            "conversation": cls.conversation(

                context.get(
                    "conversation",
                    [],
                ),

                limits["conversation"],

            ),

            "session": deepcopy(

                context.get(
                    "session",
                    {},
                )

            ),

            "long_term": cls.long_term(

                context.get(
                    "long_term",
                    [],
                ),

                limits["long_term"],

            ),

            "semantic": cls.semantic(

                context.get(
                    "semantic",
                    [],
                ),

                limits["semantic"],

            ),

        }

    # -------------------------------------------------
    # Conversation
    # -------------------------------------------------

    @staticmethod
    def conversation(
        messages,
        limit,
    ):

        if not messages:

            return []

        return deepcopy(

            messages[-limit:]

        )

    # -------------------------------------------------
    # Long-Term Memory
    # -------------------------------------------------

    @staticmethod
    def long_term(
        memories,
        limit,
    ):

        if not memories:

            return []

        ranked = sorted(

            memories,

            key=lambda m: (

                m.get(
                    "pinned",
                    False,
                ),

                m.get(
                    "importance",
                    0,
                ),

                m.get(
                    "updated_at",
                    0,
                ),

            ),

            reverse=True,

        )

        return deepcopy(

            ranked[:limit]

        )

    # -------------------------------------------------
    # Semantic Memory
    # -------------------------------------------------

    @staticmethod
    def semantic(
        memories,
        limit,
    ):

        if not memories:

            return []

        ranked = sorted(

            memories,

            key=lambda m: (

                m.get(
                    "importance",
                    0,
                ),

                m.get(
                    "created_at",
                    0,
                ),

            ),

            reverse=True,

        )

        return deepcopy(

            ranked[:limit]

        )

    # -------------------------------------------------
    # Counts
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
        selected,
    ):

        return {

            "conversation": len(

                selected.get(
                    "conversation",
                    [],
                )

            ),

            "session": len(

                selected.get(
                    "session",
                    {},
                )

            ),

            "long_term": len(

                selected.get(
                    "long_term",
                    [],
                )

            ),

            "semantic": len(

                selected.get(
                    "semantic",
                    [],
                )

            ),

            "total": (

                len(
                    selected.get(
                        "conversation",
                        [],
                    )
                )

                +

                len(
                    selected.get(
                        "session",
                        {},
                    )
                )

                +

                len(
                    selected.get(
                        "long_term",
                        [],
                    )
                )

                +

                len(
                    selected.get(
                        "semantic",
                        [],
                    )
                )

            ),

        }

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return {

            "conversation": [],

            "session": {},

            "long_term": [],

            "semantic": [],

        }

    # -------------------------------------------------
    # Has Context
    # -------------------------------------------------

    @classmethod
    def has_context(
        cls,
        selected,
    ):

        return any(

            [

                selected.get(
                    "conversation"
                ),

                selected.get(
                    "session"
                ),

                selected.get(
                    "long_term"
                ),

                selected.get(
                    "semantic"
                ),

            ]

        )