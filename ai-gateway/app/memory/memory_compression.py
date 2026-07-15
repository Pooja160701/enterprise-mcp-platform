from copy import deepcopy
from collections import Counter


class MemoryCompression:
    """
    Enterprise Memory Compression

    Compresses long conversation histories before
    they are sent to the LLM.

    Features

    ✓ Removes duplicate messages
    ✓ Removes empty messages
    ✓ Merges consecutive messages
    ✓ Keeps important memories
    ✓ Token estimation
    ✓ Configurable limits
    """

    DEFAULT_MAX_MESSAGES = 25

    DEFAULT_MAX_CHARS = 6000

    # --------------------------------------------------
    # Compress
    # --------------------------------------------------

    @classmethod
    def compress(
        cls,
        history,
        max_messages=None,
        max_chars=None,
    ):

        max_messages = (
            max_messages
            or cls.DEFAULT_MAX_MESSAGES
        )

        max_chars = (
            max_chars
            or cls.DEFAULT_MAX_CHARS
        )

        history = deepcopy(history)

        #
        # Remove empty
        #

        history = cls.remove_empty(
            history,
        )

        #
        # Remove duplicates
        #

        history = cls.remove_duplicates(
            history,
        )

        #
        # Merge consecutive roles
        #

        history = cls.merge_messages(
            history,
        )

        #
        # Sort by importance
        #

        important = cls.keep_important(
            history,
            max_messages,
        )

        #
        # Trim by character budget
        #

        important = cls.trim_characters(
            important,
            max_chars,
        )

        return important

    # --------------------------------------------------
    # Remove Empty
    # --------------------------------------------------

    @staticmethod
    def remove_empty(
        history,
    ):

        return [

            message

            for message in history

            if str(
                message.get(
                    "content",
                    "",
                )
            ).strip()

        ]

    # --------------------------------------------------
    # Remove Duplicate Messages
    # --------------------------------------------------

    @staticmethod
    def remove_duplicates(
        history,
    ):

        seen = set()

        result = []

        for message in history:

            key = (

                message.get(
                    "role",
                    "",
                ),

                message.get(
                    "content",
                    "",
                ).strip(),

            )

            if key in seen:

                continue

            seen.add(key)

            result.append(message)

        return result

    # --------------------------------------------------
    # Merge Consecutive Messages
    # --------------------------------------------------

    @staticmethod
    def merge_messages(
        history,
    ):

        if not history:

            return []

        merged = [

            deepcopy(
                history[0]
            )

        ]

        for message in history[1:]:

            previous = merged[-1]

            if (

                previous["role"]

                ==

                message["role"]

            ):

                previous["content"] += (

                    "\n"

                    + message["content"]

                )

            else:

                merged.append(

                    deepcopy(message)

                )

        return merged

    # --------------------------------------------------
    # Importance Ranking
    # --------------------------------------------------

    @staticmethod
    def importance(
        message,
    ):

        score = 0

        score += message.get(
            "importance",
            50,
        )

        if message["role"] == "user":

            score += 10

        if message["role"] == "assistant":

            score += 5

        if message["role"] == "tool_result":

            score += 15

        if message.get(
            "pinned",
            False,
        ):

            score += 25

        return score

    # --------------------------------------------------
    # Keep Important
    # --------------------------------------------------

    @classmethod
    def keep_important(
        cls,
        history,
        limit,
    ):

        history.sort(

            key=cls.importance,

            reverse=True,

        )

        selected = history[:limit]

        #
        # Restore chronological order
        #

        selected.sort(

            key=lambda x: x.get(
                "timestamp",
                0,
            )

        )

        return selected

    # --------------------------------------------------
    # Character Budget
    # --------------------------------------------------

    @staticmethod
    def trim_characters(
        history,
        max_chars,
    ):

        total = 0

        result = []

        for message in history:

            length = len(
                message["content"]
            )

            if total + length > max_chars:

                break

            total += length

            result.append(message)

        return result

    # --------------------------------------------------
    # Token Estimate
    # --------------------------------------------------

    @staticmethod
    def estimate_tokens(
        history,
    ):

        chars = sum(

            len(

                message.get(
                    "content",
                    "",
                )

            )

            for message in history

        )

        return chars // 4

    # --------------------------------------------------
    # Summary Statistics
    # --------------------------------------------------

    @classmethod
    def statistics(
        cls,
        original,
        compressed,
    ):

        before_chars = sum(

            len(

                message.get(
                    "content",
                    "",
                )

            )

            for message in original

        )

        after_chars = sum(

            len(

                message.get(
                    "content",
                    "",
                )

            )

            for message in compressed

        )

        before_tokens = cls.estimate_tokens(
            original,
        )

        after_tokens = cls.estimate_tokens(
            compressed,
        )

        roles = Counter(

            message["role"]

            for message in compressed

        )

        return {

            "messages_before": len(original),

            "messages_after": len(compressed),

            "characters_before": before_chars,

            "characters_after": after_chars,

            "tokens_before": before_tokens,

            "tokens_after": after_tokens,

            "compression_ratio": round(

                after_chars / max(
                    1,
                    before_chars,
                ),

                3,

            ),

            "roles": dict(roles),

        }