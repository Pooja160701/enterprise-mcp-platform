from copy import deepcopy
from difflib import SequenceMatcher
from time import time


class MemoryRanker:
    """
    Enterprise Memory Ranker

    Scores memories for retrieval.

    Ranking Factors

    ✓ Semantic Similarity
    ✓ Importance
    ✓ Recency
    ✓ Usage Frequency
    ✓ Pinned Memory
    ✓ Category Boost

    Final Score

        similarity
      + importance
      + recency
      + frequency
      + pinned
      + category
    """

    CATEGORY_BOOST = {

        "preference": 10,

        "profile": 8,

        "fact": 7,

        "general": 5,

    }

    # --------------------------------------------------
    # Similarity
    # --------------------------------------------------

    @staticmethod
    def similarity(
        query,
        text,
    ):

        return SequenceMatcher(

            None,

            query.lower(),

            text.lower(),

        ).ratio()

    # --------------------------------------------------
    # Rank Memories
    # --------------------------------------------------

    @classmethod
    def rank(
        cls,
        query,
        memories,
        top_k=10,
    ):

        ranked = []

        now = time()

        for memory in memories:

            score = 0.0

            #
            # ------------------------------------
            # Similarity (0-50)
            # ------------------------------------
            #

            similarity = cls.similarity(

                query,

                memory.get(
                    "content",
                    "",
                ),

            )

            score += similarity * 50

            #
            # ------------------------------------
            # Importance (0-20)
            # ------------------------------------
            #

            importance = memory.get(

                "importance",

                50,

            )

            score += importance * 0.20

            #
            # ------------------------------------
            # Recency (0-10)
            # ------------------------------------
            #

            created = memory.get(

                "created_at",

                now,

            )

            age_hours = (

                now - created

            ) / 3600

            recency = max(

                0,

                10 - age_hours,

            )

            score += recency

            #
            # ------------------------------------
            # Usage Frequency (0-10)
            # ------------------------------------
            #

            score += min(

                10,

                memory.get(
                    "access_count",
                    0,
                ),

            )

            #
            # ------------------------------------
            # Pinned (10)
            # ------------------------------------
            #

            if memory.get(

                "pinned",

                False,

            ):

                score += 10

            #
            # ------------------------------------
            # Category Boost
            # ------------------------------------
            #

            category = memory.get(

                "category",

                "general",

            )

            score += cls.CATEGORY_BOOST.get(

                category,

                0,

            )

            ranked_memory = deepcopy(memory)

            ranked_memory["score"] = round(

                score,

                2,

            )

            ranked_memory["similarity"] = round(

                similarity,

                3,

            )

            ranked.append(

                ranked_memory

            )

        ranked.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        return ranked[:top_k]

    # --------------------------------------------------
    # Best Memory
    # --------------------------------------------------

    @classmethod
    def best(
        cls,
        query,
        memories,
    ):

        ranked = cls.rank(

            query,

            memories,

            top_k=1,

        )

        if ranked:

            return ranked[0]

        return None

    # --------------------------------------------------
    # Update Access Count
    # --------------------------------------------------

    @staticmethod
    def touch(
        memory,
    ):

        memory["access_count"] = (

            memory.get(

                "access_count",

                0,

            )

            + 1

        )

        memory["last_accessed"] = time()

        return memory

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @staticmethod
    def statistics(
        memories,
    ):

        if not memories:

            return {

                "count": 0,

                "average_score": 0,

                "average_importance": 0,

            }

        avg_importance = sum(

            m.get(

                "importance",

                50,

            )

            for m in memories

        ) / len(memories)

        avg_score = sum(

            m.get(

                "score",

                0,

            )

            for m in memories

        ) / len(memories)

        return {

            "count": len(memories),

            "average_score": round(

                avg_score,

                2,

            ),

            "average_importance": round(

                avg_importance,

                2,

            ),

        }