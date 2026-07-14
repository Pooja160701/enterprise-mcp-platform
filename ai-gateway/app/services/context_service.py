class ContextStore:
    """
    Stores conversation context.

    Example:

    conversation_id ->
    {
        "repository": "...",
        "database": "...",
        "schema": "...",
        "directory": "...",
        "file": "...",
        "namespace": "..."
    }
    """

    _store = {}

    @classmethod
    def get(cls, conversation):

        return cls._store.setdefault(
            conversation,
            {}
        )

    @classmethod
    def update(
        cls,
        conversation,
        **kwargs,
    ):

        memory = cls.get(conversation)

        for key, value in kwargs.items():

            if value is not None:
                memory[key] = value

    @classmethod
    def clear(
        cls,
        conversation,
    ):

        cls._store.pop(
            conversation,
            None,
        )