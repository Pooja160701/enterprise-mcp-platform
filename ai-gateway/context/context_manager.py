from copy import deepcopy

from context.context_builder import ContextBuilder
from context.context_selector import ContextSelector
from context.context_prioritization import ContextPrioritization
from context.context_compression import ContextCompression
from context.token_budget_manager import TokenBudgetManager
from context.prompt_context import PromptContext


class ContextManager:
    """
    Enterprise Context Manager

    Complete Context Pipeline

        ContextBuilder
              │
              ▼
        ContextSelector
              │
              ▼
    ContextPrioritization
              │
              ▼
     ContextCompression
              │
              ▼
    TokenBudgetManager
              │
              ▼
        PromptContext

    Single entry point used by AgentService.
    """

    # -------------------------------------------------
    # Build Prompt Context
    # -------------------------------------------------

    @classmethod
    def build(
        cls,
        user_query,
        conversation_id=None,
        user_id=None,
        system_prompt=None,
        token_budget=None,
    ):

        #
        # Step 1
        #

        raw_context = ContextBuilder.build(

            conversation_id=conversation_id,

            user_id=user_id,

        )

        #
        # Step 2
        #

        selected = ContextSelector.select(

            raw_context,

        )

        #
        # Step 3
        #

        prioritized = ContextPrioritization.prioritize(

            selected,

        )

        #
        # Step 4
        #

        compressed = ContextCompression.compress(

            prioritized,

        )

        #
        # Step 5
        #

        budgeted = TokenBudgetManager.apply(

            compressed,

            budget=token_budget,

        )

        #
        # Step 6
        #

        prompt = PromptContext.build(

            selected_context=budgeted,

            user_query=user_query,

            system_prompt=system_prompt,

        )

        return prompt

    # -------------------------------------------------
    # Build Context (Enterprise API)
    # -------------------------------------------------

    @classmethod
    def build_context(
        cls,
        query,
        conversation_id=None,
        user_id=None,
        system_prompt=None,
        token_budget=None,
    ):
        """
        Enterprise API.

        Returns the final rendered prompt string.
        """

        prompt_context = cls.build(
            user_query=query,
            conversation_id=conversation_id,
            user_id=user_id,
            system_prompt=system_prompt,
            token_budget=token_budget,
        )

        return PromptContext.render(
            prompt_context,
        )
    
    # -------------------------------------------------
    # Render Prompt
    # -------------------------------------------------

    @classmethod
    def render(
        cls,
        **kwargs,
    ):

        prompt = cls.build(

            **kwargs,

        )

        return PromptContext.render(

            prompt,

        )

    # -------------------------------------------------
    # OpenAI Messages
    # -------------------------------------------------

    @classmethod
    def messages(
        cls,
        **kwargs,
    ):

        prompt = cls.build(

            **kwargs,

        )

        return PromptContext.messages(

            prompt,

        )

    # -------------------------------------------------
    # Pipeline
    # -------------------------------------------------

    @classmethod
    def pipeline(
        cls,
        conversation_id=None,
        user_id=None,
    ):

        raw = ContextBuilder.build(

            conversation_id,

            user_id,

        )

        selected = ContextSelector.select(

            raw,

        )

        prioritized = ContextPrioritization.prioritize(

            selected,

        )

        compressed = ContextCompression.compress(

            prioritized,

        )

        budgeted = TokenBudgetManager.apply(

            compressed,

        )

        return {

            "raw": deepcopy(raw),

            "selected": deepcopy(selected),

            "prioritized": deepcopy(prioritized),

            "compressed": deepcopy(compressed),

            "budgeted": deepcopy(budgeted),

        }

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
        prompt,
    ):
        """
        Statistics for a rendered prompt.
        """

        if not prompt:

            return {

                "characters": 0,

                "words": 0,

                "estimated_tokens": 0,

            }

        return {

            "characters": len(prompt),

            "words": len(prompt.split()),

            "estimated_tokens": len(prompt) // 4,

        }

    # -------------------------------------------------
    # Estimated Tokens
    # -------------------------------------------------

    @staticmethod
    def tokens(
        prompt,
    ):
        if not prompt:

            return 0

        return max(
            1,
            len(prompt) // 4,
        )
    
    # -------------------------------------------------
    # Empty Prompt
    # -------------------------------------------------

    @staticmethod
    def empty():

        return PromptContext.empty()

    # -------------------------------------------------
    # Has Context
    # -------------------------------------------------

    @classmethod
    def has_context(
        cls,
        conversation_id=None,
        user_id=None,
    ):

        context = ContextBuilder.build(

            conversation_id,

            user_id,

        )

        return ContextBuilder.has_context(

            context,

        )