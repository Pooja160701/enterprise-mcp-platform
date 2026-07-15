from copy import deepcopy


class PromptContext:
    """
    Enterprise Prompt Context

    Converts selected context into the final prompt
    consumed by the LLM.

    Sections

    ✓ System Context
    ✓ Session Memory
    ✓ Long-Term Memory
    ✓ Semantic Memory
    ✓ Conversation History
    ✓ User Query

    Ready for

    ✓ OpenAI
    ✓ Anthropic
    ✓ Gemini
    ✓ Ollama
    ✓ Azure OpenAI
    """

    # -------------------------------------------------
    # Build Prompt Context
    # -------------------------------------------------

    @classmethod
    def build(
        cls,
        selected_context=None,
        user_query=None,
        system_prompt=None,
        *,
        context=None,
        query=None,
    ):
        """
        Supports both APIs.

        Old:

            PromptContext.build(
                selected_context,
                user_query,
            )

        New:

            PromptContext.build(
                context=context,
                query=query,
            )
        """

        if context is not None:
            selected_context = context

        if query is not None:
            user_query = query

        selected_context = selected_context or {}

        prompt_context = {

            "system": system_prompt or "",

            "session": deepcopy(
                selected_context.get(
                    "session",
                    {},
                )
            ),

            "long_term": deepcopy(
                selected_context.get(
                    "long_term",
                    [],
                )
            ),

            "semantic": deepcopy(
                selected_context.get(
                    "semantic",
                    [],
                )
            ),

            "conversation": deepcopy(
                selected_context.get(
                    "conversation",
                    [],
                )
            ),

            "user_query": user_query or "",

        }

        return prompt_context
    
    # -------------------------------------------------
    # Render Prompt
    # -------------------------------------------------

    @classmethod
    def render(
        cls,
        prompt_context,
    ):

        lines = []

        #
        # System
        #

        system = prompt_context.get(
            "system",
            "",
        )

        if system:

            lines.append("=== SYSTEM ===")
            lines.append(system)
            lines.append("")

        #
        # Session
        #

        session = prompt_context.get(
            "session",
            {},
        )

        if session:

            lines.append("=== SESSION MEMORY ===")

            #
            # Raw dictionary
            #
            if isinstance(session, dict):

                for key, value in session.items():

                    lines.append(
                        f"{key}: {value}"
                    )

            #
            # Prioritized list
            #
            elif isinstance(session, list):

                for item in session:

                    lines.append(
                        f"{item.get('key', '')}: {item.get('value', '')}"
                    )

            lines.append("")

        #
        # Long-Term Memory
        #

        memories = prompt_context.get(
            "long_term",
            [],
        )

        if memories:

            lines.append(
                "=== LONG-TERM MEMORY ==="
            )

            for memory in memories:

                lines.append(

                    f"- {memory['content']}"

                )

            lines.append("")

        #
        # Semantic Memory
        #

        semantic = prompt_context.get(
            "semantic",
            [],
        )

        if semantic:

            lines.append(
                "=== SEMANTIC MEMORY ==="
            )

            for memory in semantic:

                lines.append(

                    f"- {memory['content']}"

                )

            lines.append("")

        #
        # Conversation
        #

        history = prompt_context.get(
            "conversation",
            [],
        )

        if history:

            lines.append(
                "=== CONVERSATION ==="
            )

            for message in history:

                role = message.get(
                    "role",
                    "unknown",
                )

                content = message.get(
                    "content",
                    "",
                )

                lines.append(

                    f"{role.upper()}: {content}"

                )

            lines.append("")

        #
        # User Query
        #

        lines.append("=== USER QUERY ===")

        lines.append(

            prompt_context.get(
                "user_query",
                "",
            )

        )

        return "\n".join(lines)

    # -------------------------------------------------
    # OpenAI Messages
    # -------------------------------------------------

    @classmethod
    def messages(
        cls,
        prompt_context,
    ):

        messages = []

        system = prompt_context.get(
            "system",
            "",
        )

        if system:

            messages.append(

                {

                    "role": "system",

                    "content": system,

                }

            )

        #
        # Context
        #

        context = cls.render(
            prompt_context,
        )

        messages.append(

            {

                "role": "user",

                "content": context,

            }

        )

        return messages

    # -------------------------------------------------
    # Token Estimation
    # -------------------------------------------------

    @staticmethod
    def tokens(prompt):
        """
        Rough token estimation.

        OpenAI average:
            1 token ≈ 4 characters
        """

        if not prompt:
            return 0

        return max(
            1,
            len(prompt) // 4,
        )
    
    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
        prompt_context,
    ):

        rendered = cls.render(
            prompt_context,
        )

        #
        # Session can be either:
        #   dict  -> raw context
        #   list  -> prioritized context
        #

        session = prompt_context.get(
            "session",
            {},
        )

        if isinstance(session, dict):

            session_count = len(session)

        elif isinstance(session, list):

            session_count = len(session)

        else:

            session_count = 0

        return {

            "characters": len(
                rendered,
            ),

            "words": len(
                rendered.split(),
            ),

            "estimated_tokens": len(
                rendered
            ) // 4,

            "conversation": len(

                prompt_context.get(
                    "conversation",
                    [],
                )

            ),

            "semantic": len(

                prompt_context.get(
                    "semantic",
                    [],
                )

            ),

            "long_term": len(

                prompt_context.get(
                    "long_term",
                    [],
                )

            ),

            "session": session_count,

        }

    # -------------------------------------------------
    # Empty Prompt
    # -------------------------------------------------

    @staticmethod
    def empty():

        return {

            "system": "",

            "session": {},

            "long_term": [],

            "semantic": [],

            "conversation": [],

            "user_query": "",

        }