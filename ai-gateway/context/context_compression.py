from copy import deepcopy


class ContextCompression:
    """
    Enterprise Context Compression

    Compresses context before token budgeting.

    Features

    ✓ Remove duplicate messages
    ✓ Keep latest conversation
    ✓ Keep highest-importance memories
    ✓ Compress semantic memories
    ✓ Configurable limits

    Pipeline

        Context Builder
              │
              ▼
        Context Selector
              │
              ▼
      Context Compression
              │
              ▼
     Token Budget Manager
              │
              ▼
        Prompt Context
    """

    DEFAULT_LIMITS = {

        "conversation": 8,

        "long_term": 5,

        "semantic": 5,

    }

    # -------------------------------------------------
    # Compress
    # -------------------------------------------------

    @classmethod
    def compress(
        cls,
        context,
        limits=None,
    ):

        limits = {

            **cls.DEFAULT_LIMITS,

            **(limits or {}),

        }

        compressed = deepcopy(context)

        compressed["conversation"] = cls.compress_conversation(

            compressed.get(
                "conversation",
                [],
            ),

            limits["conversation"],

        )

        compressed["long_term"] = cls.compress_long_term(

            compressed.get(
                "long_term",
                [],
            ),

            limits["long_term"],

        )

        compressed["semantic"] = cls.compress_semantic(

            compressed.get(
                "semantic",
                [],
            ),

            limits["semantic"],

        )

        return compressed

    # -------------------------------------------------
    # Conversation
    # -------------------------------------------------

    @staticmethod
    def compress_conversation(
        conversation,
        limit,
    ):

        if not conversation:

            return []

        seen = set()

        unique = []

        #
        # Keep newest messages
        #

        for message in reversed(conversation):

            content = message.get(

                "content",

                "",

            ).strip().lower()

            if content in seen:

                continue

            seen.add(content)

            unique.append(message)

        unique.reverse()

        return deepcopy(

            unique[-limit:]

        )

    # -------------------------------------------------
    # Long-Term Memory
    # -------------------------------------------------

    @staticmethod
    def compress_long_term(
        memories,
        limit,
    ):

        if not memories:

            return []

        ranked = sorted(

            memories,

            key=lambda m: (

                m.get(
                    "pinned",
                    False,
                ),

                m.get(
                    "importance",
                    0,
                ),

                m.get(
                    "updated_at",
                    0,
                ),

            ),

            reverse=True,

        )

        return deepcopy(

            ranked[:limit]

        )

    # -------------------------------------------------
    # Semantic Memory
    # -------------------------------------------------

    @staticmethod
    def compress_semantic(
        memories,
        limit,
    ):

        if not memories:

            return []

        ranked = sorted(

            memories,

            key=lambda m: (

                m.get(
                    "importance",
                    0,
                ),

                m.get(
                    "created_at",
                    0,
                ),

            ),

            reverse=True,

        )

        seen = set()

        result = []

        for memory in ranked:

            content = memory.get(

                "content",

                "",

            ).strip().lower()

            if content in seen:

                continue

            seen.add(content)

            result.append(memory)

            if len(result) >= limit:

                break

        return deepcopy(result)

    # -------------------------------------------------
    # Compression Ratio
    # -------------------------------------------------

    @classmethod
    def ratio(
        cls,
        original,
        compressed,
    ):

        before = cls.count(original)

        after = cls.count(compressed)

        if before == 0:

            return 1.0

        return round(

            after / before,

            2,

        )

    # -------------------------------------------------
    # Count Items
    # -------------------------------------------------

    @staticmethod
    def count(
        context,
    ):

        return (

            len(

                context.get(
                    "conversation",
                    [],
                )

            )

            +

            len(

                context.get(
                    "session",
                    {},
                )

            )

            +

            len(

                context.get(
                    "long_term",
                    [],
                )

            )

            +

            len(

                context.get(
                    "semantic",
                    [],
                )

            )

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
        original,
        compressed,
    ):

        before = cls.count(original)

        after = cls.count(compressed)

        return {

            "before": before,

            "after": after,

            "saved": max(

                0,

                before - after,

            ),

            "compression_ratio": cls.ratio(

                original,

                compressed,

            ),

        }