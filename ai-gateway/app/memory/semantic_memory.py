from copy import deepcopy
from difflib import SequenceMatcher
from time import time


class SemanticMemory:
    """
    Enterprise Semantic Memory

    Lightweight semantic memory without embeddings.

    Features

    ✓ Similarity Search
    ✓ Keyword Search
    ✓ Tag Search
    ✓ Importance Ranking
    ✓ Recent Memory Boost
    ✓ Update/Delete
    ✓ Statistics

    Can later be replaced with
    ChromaDB / FAISS / pgvector.
    """

    _memory = []

    _next_id = 1

    # --------------------------------------------------
    # Add Memory
    # --------------------------------------------------

    @classmethod
    def add(
        cls,
        content,
        tags=None,
        importance=50,
        metadata=None,
    ):

        tags = tags or []

        metadata = metadata or {}

        memory = {

            "id": cls._next_id,

            "content": content,

            "tags": list(tags),

            "importance": importance,

            "metadata": deepcopy(metadata),

            "created_at": time(),

        }

        cls._memory.append(memory)

        cls._next_id += 1

        return deepcopy(memory)

    # --------------------------------------------------
    # Get All
    # --------------------------------------------------

    @classmethod
    def all(cls):

        return deepcopy(cls._memory)

    # --------------------------------------------------
    # Similarity
    # --------------------------------------------------

    @staticmethod
    def similarity(
        a,
        b,
    ):

        return SequenceMatcher(

            None,

            a.lower(),

            b.lower(),

        ).ratio()

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    @classmethod
    def search(
        cls,
        query,
        top_k=5,
        minimum_score=0.30,
    ):

        results = []

        for memory in cls._memory:

            score = cls.similarity(

                query,

                memory["content"],

            )

            #
            # Importance boost
            #

            score += (

                memory["importance"] / 100

            ) * 0.15

            #
            # Recent boost
            #

            age = max(

                1,

                time() - memory["created_at"],

            )

            score += (

                1 / age

            ) * 0.05

            if score >= minimum_score:

                results.append(

                    {

                        **deepcopy(memory),

                        "score": round(

                            score,

                            4,

                        ),

                    }

                )

        results.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        return results[:top_k]

    # --------------------------------------------------
    # Keyword Search
    # --------------------------------------------------

    @classmethod
    def keyword(
        cls,
        keyword,
    ):

        keyword = keyword.lower()

        matches = []

        for memory in cls._memory:

            if keyword in memory["content"].lower():

                matches.append(

                    deepcopy(memory)

                )

        return matches

    # --------------------------------------------------
    # Tag Search
    # --------------------------------------------------

    @classmethod
    def tag(
        cls,
        tag,
    ):

        return [

            deepcopy(memory)

            for memory in cls._memory

            if tag in memory["tags"]

        ]

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    @classmethod
    def update(
        cls,
        memory_id,
        **fields,
    ):

        for memory in cls._memory:

            if memory["id"] == memory_id:

                for key, value in fields.items():

                    memory[key] = value

                return deepcopy(memory)

        return None

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    @classmethod
    def delete(
        cls,
        memory_id,
    ):

        for i, memory in enumerate(cls._memory):

            if memory["id"] == memory_id:

                cls._memory.pop(i)

                return True

        return False

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    @classmethod
    def clear(cls):

        cls._memory.clear()

        cls._next_id = 1

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @classmethod
    def stats(cls):

        if not cls._memory:

            return {

                "memories": 0,

                "average_importance": 0,

                "tags": {},

            }

        tags = {}

        importance = 0

        for memory in cls._memory:

            importance += memory["importance"]

            for tag in memory["tags"]:

                tags[tag] = tags.get(

                    tag,

                    0,

                ) + 1

        return {

            "memories": len(cls._memory),

            "average_importance": round(

                importance / len(cls._memory),

                2,

            ),

            "tags": tags,

        }