from copy import deepcopy


class TokenBudgetManager:
    """
    Enterprise Token Budget Manager

    Ensures the prompt stays within the model's
    context window.

    Priority Order (Highest → Lowest)

    1. User Query
    2. Session Memory
    3. Recent Conversation
    4. Long-Term Memory
    5. Semantic Memory
    """

    CHARS_PER_TOKEN = 4

    DEFAULT_TOKEN_BUDGET = 4000

    # -------------------------------------------------
    # Estimate Tokens
    # -------------------------------------------------

    @classmethod
    def estimate_tokens(
        cls,
        text,
    ):

        if not text:
            return 0

        return max(
            1,
            len(str(text)) // cls.CHARS_PER_TOKEN,
        )

    # -------------------------------------------------
    # Estimate Context
    # -------------------------------------------------

    @classmethod
    def estimate_context(
        cls,
        context,
    ):

        total = 0

        #
        # System
        #

        total += cls.estimate_tokens(
            context.get(
                "system",
                "",
            )
        )

        #
        # User Query
        #

        total += cls.estimate_tokens(
            context.get(
                "user_query",
                "",
            )
        )

        #
        # Session Memory
        #

        session = context.get(
            "session",
            {},
        )

        # Raw dictionary
        if isinstance(session, dict):

            for key, value in session.items():

                total += cls.estimate_tokens(
                    f"{key}: {value}"
                )

        # Prioritized list
        elif isinstance(session, list):

            for item in session:

                total += cls.estimate_tokens(
                    f"{item.get('key', '')}: {item.get('value', '')}"
                )

        #
        # Conversation
        #

        for message in context.get(
            "conversation",
            [],
        ):

            total += cls.estimate_tokens(
                message.get(
                    "content",
                    "",
                )
            )

        #
        # Long-Term Memory
        #

        for memory in context.get(
            "long_term",
            [],
        ):

            total += cls.estimate_tokens(
                memory.get(
                    "content",
                    "",
                )
            )

        #
        # Semantic Memory
        #

        for memory in context.get(
            "semantic",
            [],
        ):

            total += cls.estimate_tokens(
                memory.get(
                    "content",
                    "",
                )
            )

        return total

    # -------------------------------------------------
    # Apply Budget
    # -------------------------------------------------

    @classmethod
    def apply(
        cls,
        context,
        budget=None,
    ):

        budget = budget or cls.DEFAULT_TOKEN_BUDGET

        context = deepcopy(context)

        context.setdefault("conversation", [])
        context.setdefault("session", {})
        context.setdefault("long_term", [])
        context.setdefault("semantic", [])
        context.setdefault("system", "")
        context.setdefault("user_query", "")

        #
        # Remove semantic memories first
        #

        while (
            context["semantic"]
            and cls.estimate_context(context) > budget
        ):
            context["semantic"].pop()

        #
        # Remove long-term memories
        #

        while (
            context["long_term"]
            and cls.estimate_context(context) > budget
        ):
            context["long_term"].pop()

        #
        # Trim oldest conversation messages
        #

        while (
            len(context["conversation"]) > 2
            and cls.estimate_context(context) > budget
        ):
            context["conversation"].pop(0)

        return context

    # -------------------------------------------------
    # Alias
    # -------------------------------------------------

    @classmethod
    def fit(
        cls,
        context,
        max_tokens=None,
    ):

        return cls.apply(
            context=context,
            budget=max_tokens,
        )

    # -------------------------------------------------
    # Fits Budget
    # -------------------------------------------------

    @classmethod
    def fits(
        cls,
        context,
        budget=None,
    ):

        budget = budget or cls.DEFAULT_TOKEN_BUDGET

        return (
            cls.estimate_context(context)
            <= budget
        )

    # -------------------------------------------------
    # Remaining Tokens
    # -------------------------------------------------

    @classmethod
    def remaining(
        cls,
        context,
        budget=None,
    ):

        budget = budget or cls.DEFAULT_TOKEN_BUDGET

        return max(
            0,
            budget - cls.estimate_context(context),
        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
        context,
        budget=None,
    ):

        budget = budget or cls.DEFAULT_TOKEN_BUDGET

        used = cls.estimate_context(context)

        return {

            "budget": budget,

            "used": used,

            "remaining": max(
                0,
                budget - used,
            ),

            "utilization": round(
                (used / budget) * 100,
                2,
            ),

            "fits": used <= budget,

        }

    # -------------------------------------------------
    # Set Budget
    # -------------------------------------------------

    @classmethod
    def set_budget(
        cls,
        budget,
    ):

        cls.DEFAULT_TOKEN_BUDGET = budget

    # -------------------------------------------------
    # Get Budget
    # -------------------------------------------------

    @classmethod
    def get_budget(
        cls,
    ):

        return cls.DEFAULT_TOKEN_BUDGET