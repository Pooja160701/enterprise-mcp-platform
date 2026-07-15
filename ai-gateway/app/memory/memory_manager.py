from copy import deepcopy

from app.memory.conversation_history import ConversationHistory
from app.memory.long_term_memory import LongTermMemory
from app.memory.memory_compression import MemoryCompression
from app.memory.memory_search import MemorySearch
from app.memory.memory_store import MemoryStore
from app.memory.memory_summarizer import MemorySummarizer
from app.memory.semantic_memory import SemanticMemory
from app.memory.session_memory import SessionMemory


class MemoryManager:
    """
    Enterprise Memory Manager

                    MemoryManager
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
    Conversation      Session          Long-Term
       History         Memory            Memory
        │                 │                  │
        └──────────────┬──┴──────────────┐
                       │
                 Semantic Memory
                       │
                 Memory Search
                       │
            Compression & Summary

    Single entry point used by AgentService.
    """

    # -------------------------------------------------
    # Conversation
    # -------------------------------------------------

    @classmethod
    def add_message(
        cls,
        conversation_id,
        role,
        content,
        importance=50,
        metadata=None,
    ):

        metadata = metadata or {}

        #
        # Preserve importance inside metadata because
        # ConversationHistory does not have an
        # importance field.
        #

        metadata.setdefault(
            "importance",
            importance,
        )

        return ConversationHistory.add(

            conversation_id=conversation_id,

            role=role,

            content=content,

            metadata=metadata,

        )

    @classmethod
    def history(
        cls,
        conversation_id,
    ):

        return ConversationHistory.get(
            conversation_id
        )

    # -------------------------------------------------
    # Session Memory
    # -------------------------------------------------

    @classmethod
    def set_session(
        cls,
        conversation_id,
        key,
        value,
    ):

        return SessionMemory.set(

            conversation_id,

            key,

            value,

        )

    @classmethod
    def get_session(
        cls,
        conversation_id,
        key,
        default=None,
    ):

        return SessionMemory.get(

            conversation_id,

            key,

            default,

        )

    @classmethod
    def session(
        cls,
        conversation_id,
    ):

        return SessionMemory.all(
            conversation_id
        )

    # -------------------------------------------------
    # Long-Term Memory
    # -------------------------------------------------

    @classmethod
    def remember(
        cls,
        user_id,
        content,
        category="general",
        importance=50,
        pinned=False,
        metadata=None,
    ):

        return LongTermMemory.add(

            user_id=user_id,

            content=content,

            category=category,

            importance=importance,

            pinned=pinned,

            metadata=metadata or {},

        )

    @classmethod
    def memories(
        cls,
        user_id,
    ):

        return LongTermMemory.get(
            user_id
        )

    # -------------------------------------------------
    # Semantic Memory
    # -------------------------------------------------

    @classmethod
    def add_semantic(
        cls,
        text,
        metadata=None,
        tags=None,
        importance=50,
    ):

        return SemanticMemory.add(

            content=text,

            tags=tags or [],

            importance=importance,

            metadata=metadata or {},

        )

    @classmethod
    def semantic(
        cls,
    ):

        return SemanticMemory.all()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    @classmethod
    def search(
        cls,
        query,
        conversation_id=None,
        user_id=None,
        top_k=10,
    ):

        return MemorySearch.search(

            query=query,

            conversation_id=conversation_id,

            user_id=user_id,

            top_k=top_k,

        )

    @classmethod
    def best_match(
        cls,
        query,
        conversation_id=None,
        user_id=None,
    ):

        return MemorySearch.best(

            query=query,

            conversation_id=conversation_id,

            user_id=user_id,

        )

    # -------------------------------------------------
    # Compression
    # -------------------------------------------------

    @classmethod
    def compressed_history(
        cls,
        conversation_id,
        max_messages=25,
        max_chars=6000,
    ):

        history = ConversationHistory.get(
            conversation_id
        )

        return MemoryCompression.compress(

            history,

            max_messages=max_messages,

            max_chars=max_chars,

        )

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    @classmethod
    def summary(
        cls,
        conversation_id,
    ):

        history = cls.compressed_history(
            conversation_id
        )

        return MemorySummarizer.summarize(
            history
        )

    @classmethod
    def brief_summary(
        cls,
        conversation_id,
    ):

        history = cls.compressed_history(
            conversation_id
        )

        return MemorySummarizer.brief(
            history
        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    @classmethod
    def export(
        cls,
        conversation_id,
        user_id=None,
    ):

        return {

            "conversation": deepcopy(

                ConversationHistory.get(
                    conversation_id
                )

            ),

            "session": deepcopy(

                SessionMemory.all(
                    conversation_id
                )

            ),

            "semantic": deepcopy(

                SemanticMemory.all()

            ),

            "long_term": deepcopy(

                LongTermMemory.get(
                    user_id
                )

                if user_id

                else []

            ),

        }

    # -------------------------------------------------
    # Import
    # -------------------------------------------------

    @classmethod
    def load(
        cls,
        conversation_id,
        data,
    ):

        for message in data.get(
            "conversation",
            [],
        ):

            ConversationHistory.add(

                conversation_id,

                role=message["role"],

                content=message["content"],

                importance=message.get(
                    "importance",
                    50,
                ),

                metadata=message.get(
                    "metadata",
                    {},
                ),

            )

        for key, value in data.get(
            "session",
            {},
        ).items():

            SessionMemory.set(

                conversation_id,

                key,

                value,

            )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    @classmethod
    def clear_conversation(
        cls,
        conversation_id,
    ):

        ConversationHistory.clear(
            conversation_id
        )

        SessionMemory.clear(
            conversation_id
        )

    @classmethod
    def clear_all(
        cls,
    ):

        ConversationHistory.clear()

        SessionMemory.clear()

        SemanticMemory.clear()

        LongTermMemory.clear()

        MemoryStore.clear()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def stats(
        cls,
        conversation_id=None,
        user_id=None,
    ):

        return {

            "conversation": (

                len(

                    ConversationHistory.get(
                        conversation_id
                    )

                )

                if conversation_id

                else 0

            ),

            "session": (

                len(

                    SessionMemory.all(
                        conversation_id
                    )

                )

                if conversation_id

                else 0

            ),

            "semantic": len(
                SemanticMemory.all()
            ),

            "long_term": (

                len(

                    LongTermMemory.get(
                        user_id
                    )

                )

                if user_id

                else 0

            ),

            "search": MemorySearch.stats(

                conversation_id,

                user_id,

            ),

            "store": MemoryStore.stats(),

        }