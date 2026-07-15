from copy import deepcopy
from time import time


class ConversationHistory:
    """
    Enterprise Conversation History

    Stores complete conversations.

    Features

    ✓ User messages
    ✓ Assistant messages
    ✓ Tool calls
    ✓ Tool results
    ✓ Chronological ordering
    ✓ Message editing
    ✓ Deletion
    ✓ Statistics
    """

    _history = {}

    _next_message_id = 1

    # -------------------------------------------------
    # Internal
    # -------------------------------------------------

    @classmethod
    def _conversation(
        cls,
        conversation_id,
    ):

        return cls._history.setdefault(
            conversation_id,
            [],
        )

    # -------------------------------------------------
    # Generic Add
    # -------------------------------------------------

    @classmethod
    def add(
        cls,
        conversation_id,
        role,
        content,
        metadata=None,
    ):

        metadata = metadata or {}

        message = {

            "id": cls._next_message_id,

            "role": role,

            "content": content,

            "metadata": deepcopy(metadata),

            "timestamp": time(),

        }

        cls._conversation(
            conversation_id,
        ).append(message)

        cls._next_message_id += 1

        return deepcopy(message)

    # -------------------------------------------------
    # User
    # -------------------------------------------------

    @classmethod
    def add_user(
        cls,
        conversation_id,
        message,
    ):

        return cls.add(

            conversation_id,

            role="user",

            content=message,

        )

    # -------------------------------------------------
    # Assistant
    # -------------------------------------------------

    @classmethod
    def add_assistant(
        cls,
        conversation_id,
        message,
    ):

        return cls.add(

            conversation_id,

            role="assistant",

            content=message,

        )

    # -------------------------------------------------
    # Tool Call
    # -------------------------------------------------

    @classmethod
    def add_tool_call(
        cls,
        conversation_id,
        server,
        tool,
        arguments,
    ):

        return cls.add(

            conversation_id,

            role="tool_call",

            content=f"{server}.{tool}",

            metadata={

                "server": server,

                "tool": tool,

                "arguments": deepcopy(arguments),

            },

        )

    # -------------------------------------------------
    # Tool Result
    # -------------------------------------------------

    @classmethod
    def add_tool_result(
        cls,
        conversation_id,
        server,
        tool,
        result,
    ):

        return cls.add(

            conversation_id,

            role="tool_result",

            content=str(result),

            metadata={

                "server": server,

                "tool": tool,

            },

        )

    # -------------------------------------------------
    # Get Conversation
    # -------------------------------------------------

    @classmethod
    def get(
        cls,
        conversation_id,
    ):

        return deepcopy(

            cls._history.get(

                conversation_id,

                [],

            )

        )

    # -------------------------------------------------
    # Last Message
    # -------------------------------------------------

    @classmethod
    def last(
        cls,
        conversation_id,
    ):

        history = cls._history.get(

            conversation_id,

            [],

        )

        if not history:

            return None

        return deepcopy(history[-1])

    # -------------------------------------------------
    # Update Message
    # -------------------------------------------------

    @classmethod
    def update(
        cls,
        conversation_id,
        message_id,
        content,
    ):

        for message in cls._conversation(

            conversation_id,

        ):

            if message["id"] == message_id:

                message["content"] = content

                message["edited_at"] = time()

                return deepcopy(message)

        return None

    # -------------------------------------------------
    # Delete Message
    # -------------------------------------------------

    @classmethod
    def delete(
        cls,
        conversation_id,
        message_id,
    ):

        history = cls._conversation(

            conversation_id,

        )

        for index, message in enumerate(history):

            if message["id"] == message_id:

                history.pop(index)

                return True

        return False

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    @classmethod
    def clear(
        cls,
        conversation_id=None,
    ):

        if conversation_id is None:

            cls._history.clear()

            cls._next_message_id = 1

        else:

            cls._history.pop(

                conversation_id,

                None,

            )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    @classmethod
    def search(
        cls,
        conversation_id,
        keyword,
    ):

        keyword = keyword.lower()

        matches = []

        for message in cls._conversation(

            conversation_id,

        ):

            if keyword in message["content"].lower():

                matches.append(

                    deepcopy(message)

                )

        return matches

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def stats(
        cls,
    ):

        conversations = len(

            cls._history

        )

        messages = sum(

            len(history)

            for history in cls._history.values()

        )

        roles = {}

        for history in cls._history.values():

            for message in history:

                role = message["role"]

                roles[role] = roles.get(

                    role,

                    0,

                ) + 1

        return {

            "conversations": conversations,

            "messages": messages,

            "roles": roles,

        }