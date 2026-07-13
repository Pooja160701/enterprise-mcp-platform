from collections import defaultdict


class MemoryService:
    """
    Stores conversation-scoped context that can be
    reused across multiple user requests.
    """

    _memory = defaultdict(dict)

    @classmethod
    def save(
        cls,
        conversation_id: str,
        key: str,
        value,
    ):
        cls._memory[conversation_id][key] = value

    @classmethod
    def get(
        cls,
        conversation_id: str,
        key: str,
        default=None,
    ):
        return cls._memory[conversation_id].get(
            key,
            default,
        )

    @classmethod
    def get_all(
        cls,
        conversation_id: str,
    ):
        return cls._memory.get(
            conversation_id,
            {},
        )

    @classmethod
    def clear(
        cls,
        conversation_id: str,
    ):
        cls._memory.pop(
            conversation_id,
            None,
        )