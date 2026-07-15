from copy import deepcopy

from app.memory.session_memory import SessionMemory
from app.memory.semantic_memory import SemanticMemory
from app.memory.long_term_memory import LongTermMemory
from app.memory.memory_ranker import MemoryRanker


class MemorySearch:
    """
    Enterprise Memory Search

    Unified search across all memory layers.

    Search Order

        Session Memory
                ↓
        Long-Term Memory
                ↓
        Semantic Memory
                ↓
          Unified Ranking

    Features

    ✓ Cross-memory retrieval
    ✓ Ranking
    ✓ Deduplication
    ✓ Access count update
    ✓ Filters
    ✓ Top-K retrieval
    """

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

        memories = []

        #
        # ----------------------------------------
        # Session Memory
        # ----------------------------------------
        #

        if conversation_id is not None:

            session = SessionMemory.all(
                conversation_id,
            )

            for key, value in session.items():

                memories.append(

                    {

                        "id": f"session:{key}",

                        "content": str(value),

                        "category": "session",

                        "importance": 100,

                        "pinned": False,

                        "created_at": 0,

                        "source": "session",

                        "reference": key,

                    }

                )

        #
        # ----------------------------------------
        # Long-Term Memory
        # ----------------------------------------
        #

        if user_id is not None:

            memories.extend(

                deepcopy(

                    LongTermMemory.get(
                        user_id,
                    )

                )

            )

            for memory in memories:

                memory.setdefault(

                    "source",

                    "long_term",

                )

        #
        # ----------------------------------------
        # Semantic Memory
        # ----------------------------------------
        #

        semantic = SemanticMemory.all()

        for memory in semantic:

            memory = deepcopy(memory)

            memory.setdefault(

                "source",

                "semantic",

            )

            memories.append(memory)

        #
        # ----------------------------------------
        # Remove duplicates
        # ----------------------------------------
        #

        unique = []

        seen = set()

        for memory in memories:

            key = memory.get(

                "content",

                "",

            ).strip().lower()

            if key in seen:

                continue

            seen.add(key)

            unique.append(memory)

        #
        # ----------------------------------------
        # Rank
        # ----------------------------------------
        #

        ranked = MemoryRanker.rank(

            query=query,

            memories=unique,

            top_k=top_k,

        )

        #
        # ----------------------------------------
        # Update access count
        # ----------------------------------------
        #

        for memory in ranked:

            MemoryRanker.touch(
                memory,
            )

        return ranked

    # -------------------------------------------------
    # Best Match
    # -------------------------------------------------

    @classmethod
    def best(
        cls,
        query,
        conversation_id=None,
        user_id=None,
    ):

        results = cls.search(

            query=query,

            conversation_id=conversation_id,

            user_id=user_id,

            top_k=1,

        )

        if results:

            return results[0]

        return None

    # -------------------------------------------------
    # Search by Category
    # -------------------------------------------------

    @classmethod
    def category(
        cls,
        category,
        user_id,
    ):

        memories = LongTermMemory.by_category(

            user_id,

            category,

        )

        memories.sort(

            key=lambda x: (

                x.get(

                    "pinned",

                    False,

                ),

                x.get(

                    "importance",

                    50,

                ),

            ),

            reverse=True,

        )

        return memories

    # -------------------------------------------------
    # Search by Tag
    # -------------------------------------------------

    @classmethod
    def tag(
        cls,
        tag,
    ):

        return SemanticMemory.tag(tag)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def stats(
        cls,
        conversation_id=None,
        user_id=None,
    ):

        session_count = 0

        if conversation_id is not None:

            session_count = len(

                SessionMemory.all(
                    conversation_id,
                )

            )

        long_term_count = 0

        if user_id is not None:

            long_term_count = len(

                LongTermMemory.get(
                    user_id,
                )

            )

        semantic_count = len(

            SemanticMemory.all()

        )

        return {

            "session": session_count,

            "long_term": long_term_count,

            "semantic": semantic_count,

            "total": (

                session_count

                + long_term_count

                + semantic_count

            ),

        }