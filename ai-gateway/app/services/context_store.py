from typing import Any


class ContextStore:
    """
    Stores conversation context between requests.

    Structure:

    {
        conversation_id: {
            "repository": "...",
            "database": "...",
            "schema": "...",
            "table": "...",
            "directory": "...",
            "file": "...",
            "namespace": "...",
            ...
        }
    }
    """

    _store: dict[str, dict[str, Any]] = {}

    @classmethod
    def get(cls, conversation_id: str) -> dict[str, Any]:
        """
        Get (or create) context for a conversation.
        """
        if conversation_id not in cls._store:
            cls._store[conversation_id] = {}

        return cls._store[conversation_id]

    @classmethod
    def update(
        cls,
        conversation_id: str,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Update conversation context.

        Example:

        ContextStore.update(
            conversation_id,
            repository="enterprise-mcp-platform",
            file="README.md",
        )
        """

        context = cls.get(conversation_id)

        for key, value in kwargs.items():

            if value is None:
                continue

            if isinstance(value, str):

                value = value.strip()

                if value == "":
                    continue

            context[key] = value

        return context

    @classmethod
    def set(
        cls,
        conversation_id: str,
        key: str,
        value: Any,
    ) -> None:
        """
        Set a single value.
        """

        cls.get(conversation_id)[key] = value

    @classmethod
    def get_value(
        cls,
        conversation_id: str,
        key: str,
        default=None,
    ):
        """
        Retrieve one value.

        Example:

        repo = ContextStore.get_value(
            conversation,
            "repository"
        )
        """

        return cls.get(conversation_id).get(
            key,
            default,
        )

    @classmethod
    def remove(
        cls,
        conversation_id: str,
        key: str,
    ) -> None:
        """
        Remove one context value.
        """

        cls.get(conversation_id).pop(
            key,
            None,
        )

    @classmethod
    def clear(
        cls,
        conversation_id: str,
    ) -> None:
        """
        Clear all context for a conversation.
        """

        cls._store.pop(
            conversation_id,
            None,
        )

    @classmethod
    def all(cls) -> dict[str, dict[str, Any]]:
        """
        Return all stored conversations.
        Useful for debugging.
        """

        return cls._store