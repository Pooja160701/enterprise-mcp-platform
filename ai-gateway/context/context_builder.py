from copy import deepcopy

from app.memory.conversation_history import ConversationHistory
from app.memory.session_memory import SessionMemory
from app.memory.semantic_memory import SemanticMemory
from app.memory.long_term_memory import LongTermMemory


class ContextBuilder:
    """
    Enterprise Context Builder

    Collects all available context before ranking.

    Sources

    ✓ Conversation History
    ✓ Session Memory
    ✓ Long-Term Memory
    ✓ Semantic Memory

    Returns a single context object consumed by
    ContextSelector.
    """

    # -------------------------------------------------
    # Build Context
    # -------------------------------------------------

    @classmethod
    def build(
        cls,
        conversation_id=None,
        user_id=None,
    ):

        return {

            "conversation": cls.conversation(
                conversation_id,
            ),

            "session": cls.session(
                conversation_id,
            ),

            "long_term": cls.long_term(
                user_id,
            ),

            "semantic": cls.semantic(),

        }

    # -------------------------------------------------
    # Conversation
    # -------------------------------------------------

    @staticmethod
    def conversation(
        conversation_id,
    ):

        if not conversation_id:

            return []

        return deepcopy(

            ConversationHistory.get(
                conversation_id,
            )

        )

    # -------------------------------------------------
    # Session
    # -------------------------------------------------

    @staticmethod
    def session(
        conversation_id,
    ):

        if not conversation_id:

            return {}

        return deepcopy(

            SessionMemory.all(
                conversation_id,
            )

        )

    # -------------------------------------------------
    # Long-Term
    # -------------------------------------------------

    @staticmethod
    def long_term(
        user_id,
    ):

        if not user_id:

            return []

        return deepcopy(

            LongTermMemory.get(
                user_id,
            )

        )

    # -------------------------------------------------
    # Semantic
    # -------------------------------------------------

    @staticmethod
    def semantic():

        return deepcopy(

            SemanticMemory.all()

        )

    # -------------------------------------------------
    # Build Statistics
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
        context,
    ):

        return {

            "conversation_messages": len(
                context.get(
                    "conversation",
                    [],
                )
            ),

            "session_entries": len(
                context.get(
                    "session",
                    {},
                )
            ),

            "long_term_memories": len(
                context.get(
                    "long_term",
                    [],
                )
            ),

            "semantic_memories": len(
                context.get(
                    "semantic",
                    [],
                )
            ),

            "total_items": (

                len(
                    context.get(
                        "conversation",
                        [],
                    )
                )

                +

                len(
                    context.get(
                        "session",
                        {},
                    )
                )

                +

                len(
                    context.get(
                        "long_term",
                        [],
                    )
                )

                +

                len(
                    context.get(
                        "semantic",
                        [],
                    )
                )

            ),

        }

    # -------------------------------------------------
    # Empty Context
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
        context,
    ):

        return any(

            [

                context.get(
                    "conversation"
                ),

                context.get(
                    "session"
                ),

                context.get(
                    "long_term"
                ),

                context.get(
                    "semantic"
                ),

            ]

        )