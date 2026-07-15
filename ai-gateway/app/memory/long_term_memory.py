from copy import deepcopy
from time import time


class LongTermMemory:
    """
    Enterprise Long-Term Memory

    Stores durable memories that survive across
    conversations.

    Features

    ✓ User Preferences
    ✓ Facts
    ✓ Learned Information
    ✓ Importance Ranking
    ✓ Pin Memories
    ✓ Archive
    ✓ Search
    ✓ Update/Delete
    ✓ Statistics
    """

    _memory = {}

    _next_id = 1

    # --------------------------------------------
    # Internal
    # --------------------------------------------

    @classmethod
    def _user(
        cls,
        user_id,
    ):

        return cls._memory.setdefault(
            user_id,
            [],
        )

    # --------------------------------------------
    # Add Memory
    # --------------------------------------------

    @classmethod
    def add(
        cls,
        user_id,
        content,
        category="general",
        importance=50,
        pinned=False,
        metadata=None,
    ):

        metadata = metadata or {}

        memory = {

            "id": cls._next_id,

            "user_id": user_id,

            "content": content,

            "category": category,

            "importance": importance,

            "pinned": pinned,

            "archived": False,

            "metadata": deepcopy(metadata),

            "created_at": time(),

            "updated_at": time(),

        }

        cls._user(
            user_id,
        ).append(memory)

        cls._next_id += 1

        return deepcopy(memory)

    # --------------------------------------------
    # Get All
    # --------------------------------------------

    @classmethod
    def get(
        cls,
        user_id,
    ):

        return deepcopy(

            cls._memory.get(
                user_id,
                [],
            )

        )

    # --------------------------------------------
    # Get By ID
    # --------------------------------------------

    @classmethod
    def get_by_id(
        cls,
        user_id,
        memory_id,
    ):

        for memory in cls._user(
            user_id,
        ):

            if memory["id"] == memory_id:

                return deepcopy(memory)

        return None

    # --------------------------------------------
    # Search
    # --------------------------------------------

    @classmethod
    def search(
        cls,
        user_id,
        keyword,
    ):

        keyword = keyword.lower()

        matches = []

        for memory in cls._user(
            user_id,
        ):

            if memory["archived"]:
                continue

            if keyword in memory["content"].lower():

                matches.append(
                    deepcopy(memory)
                )

        matches.sort(

            key=lambda x: (

                x["pinned"],

                x["importance"],

            ),

            reverse=True,

        )

        return matches

    # --------------------------------------------
    # Category
    # --------------------------------------------

    @classmethod
    def by_category(
        cls,
        user_id,
        category,
    ):

        return [

            deepcopy(memory)

            for memory in cls._user(
                user_id,
            )

            if (

                memory["category"]

                ==

                category

            )

            and

            not memory["archived"]

        ]

    # --------------------------------------------
    # Update
    # --------------------------------------------

    @classmethod
    def update(
        cls,
        user_id,
        memory_id,
        **fields,
    ):

        for memory in cls._user(
            user_id,
        ):

            if memory["id"] == memory_id:

                for key, value in fields.items():

                    memory[key] = value

                memory["updated_at"] = time()

                return deepcopy(memory)

        return None

    # --------------------------------------------
    # Archive
    # --------------------------------------------

    @classmethod
    def archive(
        cls,
        user_id,
        memory_id,
    ):

        return cls.update(

            user_id,

            memory_id,

            archived=True,

        )

    # --------------------------------------------
    # Pin
    # --------------------------------------------

    @classmethod
    def pin(
        cls,
        user_id,
        memory_id,
    ):

        return cls.update(

            user_id,

            memory_id,

            pinned=True,

        )

    # --------------------------------------------
    # Delete
    # --------------------------------------------

    @classmethod
    def delete(
        cls,
        user_id,
        memory_id,
    ):

        memories = cls._user(
            user_id,
        )

        for i, memory in enumerate(memories):

            if memory["id"] == memory_id:

                memories.pop(i)

                return True

        return False

    # --------------------------------------------
    # Clear
    # --------------------------------------------

    @classmethod
    def clear(
        cls,
        user_id=None,
    ):

        if user_id is None:

            cls._memory.clear()

            cls._next_id = 1

        else:

            cls._memory.pop(
                user_id,
                None,
            )

    # --------------------------------------------
    # Statistics
    # --------------------------------------------

    @classmethod
    def stats(
        cls,
    ):

        users = len(cls._memory)

        memories = 0

        pinned = 0

        archived = 0

        categories = {}

        for user in cls._memory.values():

            memories += len(user)

            for memory in user:

                if memory["pinned"]:

                    pinned += 1

                if memory["archived"]:

                    archived += 1

                category = memory["category"]

                categories[category] = (

                    categories.get(

                        category,

                        0,

                    )

                    + 1

                )

        return {

            "users": users,

            "memories": memories,

            "pinned": pinned,

            "archived": archived,

            "categories": categories,

        }