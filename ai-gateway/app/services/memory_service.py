from collections import defaultdict


class MemoryService:

    _memory = defaultdict(dict)

    @classmethod
    def save(

        cls,

        conversation,

        key,

        value,

    ):

        cls._memory[conversation][key] = value

    @classmethod
    def load(

        cls,

        conversation,

        key,

    ):

        return cls._memory.get(

            conversation,

            {},

        ).get(key)

    @classmethod
    def conversation(

        cls,

        conversation,

    ):

        return cls._memory.get(

            conversation,

            {},
        )

    @classmethod
    def clear(

        cls,

        conversation,

    ):

        cls._memory.pop(

            conversation,

            None,

        )