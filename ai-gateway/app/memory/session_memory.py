from copy import deepcopy
from time import time


class SessionMemory:
    """
    Enterprise Session Memory

    Stores temporary memory for an active conversation.

    Features

    ✓ Conversation scoped
    ✓ Fast lookup
    ✓ Key-Value storage
    ✓ TTL support
    ✓ Update/Delete
    ✓ Expiration cleanup
    ✓ Statistics
    """

    _sessions = {}

    DEFAULT_TTL = 3600  # 1 hour

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    @classmethod
    def _session(
        cls,
        conversation_id,
    ):

        return cls._sessions.setdefault(
            conversation_id,
            {},
        )

    # --------------------------------------------------
    # Set
    # --------------------------------------------------

    @classmethod
    def set(
        cls,
        conversation_id,
        key,
        value,
        ttl=None,
    ):

        ttl = ttl or cls.DEFAULT_TTL

        cls._session(
            conversation_id,
        )[key] = {

            "value": deepcopy(value),

            "created_at": time(),

            "expires_at": time() + ttl,

        }

        return deepcopy(value)

    # --------------------------------------------------
    # Get
    # --------------------------------------------------

    @classmethod
    def get(
        cls,
        conversation_id,
        key,
        default=None,
    ):

        session = cls._session(
            conversation_id,
        )

        if key not in session:

            return default

        record = session[key]

        if record["expires_at"] < time():

            del session[key]

            return default

        return deepcopy(
            record["value"]
        )

    # --------------------------------------------------
    # Exists
    # --------------------------------------------------

    @classmethod
    def exists(
        cls,
        conversation_id,
        key,
    ):

        return cls.get(
            conversation_id,
            key,
        ) is not None

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    @classmethod
    def update(
        cls,
        conversation_id,
        key,
        value,
    ):

        if not cls.exists(
            conversation_id,
            key,
        ):

            return None

        cls._session(
            conversation_id,
        )[key]["value"] = deepcopy(value)

        return deepcopy(value)

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    @classmethod
    def delete(
        cls,
        conversation_id,
        key,
    ):

        session = cls._session(
            conversation_id,
        )

        if key in session:

            del session[key]

            return True

        return False

    # --------------------------------------------------
    # Cleanup Expired
    # --------------------------------------------------

    @classmethod
    def cleanup(
        cls,
        conversation_id=None,
    ):

        now = time()

        sessions = (
            [conversation_id]
            if conversation_id
            else list(cls._sessions.keys())
        )

        removed = 0

        for cid in sessions:

            session = cls._sessions.get(
                cid,
                {},
            )

            expired = [

                key

                for key, value in session.items()

                if value["expires_at"] < now

            ]

            for key in expired:

                del session[key]

                removed += 1

        return removed

    # --------------------------------------------------
    # Get Session
    # --------------------------------------------------

    @classmethod
    def all(
        cls,
        conversation_id,
    ):

        cls.cleanup(
            conversation_id,
        )

        session = {}

        for key, value in cls._session(
            conversation_id,
        ).items():

            session[key] = deepcopy(
                value["value"]
            )

        return session

    # --------------------------------------------------
    # Clear Conversation
    # --------------------------------------------------

    @classmethod
    def clear(
        cls,
        conversation_id=None,
    ):

        if conversation_id is None:

            cls._sessions.clear()

        else:

            cls._sessions.pop(
                conversation_id,
                None,
            )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @classmethod
    def stats(
        cls,
    ):

        total_sessions = len(
            cls._sessions
        )

        total_entries = sum(

            len(session)

            for session in cls._sessions.values()

        )

        return {

            "sessions": total_sessions,

            "entries": total_entries,

            "default_ttl": cls.DEFAULT_TTL,

        }