from copy import deepcopy
from time import time


class ContextPrioritization:
    """
    Enterprise Context Prioritization

    Assigns priority scores to every context item.

    Priority Factors

    ✓ Session Memory
    ✓ Pinned Memories
    ✓ Importance
    ✓ Recency
    ✓ Conversation Position
    ✓ Semantic Importance

    Used before token budgeting.
    """

    # ---------------------------------------------
    # Base Weights
    # ---------------------------------------------

    SESSION_WEIGHT = 100

    PINNED_WEIGHT = 30

    IMPORTANCE_WEIGHT = 0.40

    RECENCY_WEIGHT = 20

    RECENT_MESSAGE_WEIGHT = 15

    # ---------------------------------------------
    # Prioritize Entire Context
    # ---------------------------------------------

    @classmethod
    def prioritize(
        cls,
        context,
    ):

        context = deepcopy(context)

        context["conversation"] = cls.conversation(

            context.get(
                "conversation",
                [],
            )

        )

        context["long_term"] = cls.long_term(

            context.get(
                "long_term",
                [],
            )

        )

        context["semantic"] = cls.semantic(

            context.get(
                "semantic",
                [],
            )

        )

        context["session"] = cls.session(

            context.get(
                "session",
                {},
            )

        )

        return context

    # ---------------------------------------------
    # Session
    # ---------------------------------------------

    @classmethod
    def session(
        cls,
        session,
    ):

        ranked = []

        for key, value in session.items():

            ranked.append(

                {

                    "key": key,

                    "value": value,

                    "priority": cls.SESSION_WEIGHT,

                }

            )

        ranked.sort(

            key=lambda x: x["priority"],

            reverse=True,

        )

        return ranked

    # ---------------------------------------------
    # Conversation
    # ---------------------------------------------

    @classmethod
    def conversation(
        cls,
        conversation,
    ):

        total = len(conversation)

        ranked = []

        for index, message in enumerate(conversation):

            item = deepcopy(message)

            priority = 0

            #
            # Newer messages
            #

            priority += (

                (index + 1)

                / max(1, total)

            ) * cls.RECENT_MESSAGE_WEIGHT

            priority += (

                item.get(
                    "metadata",
                    {},
                ).get(
                    "importance",
                    50,
                )

                * 0.30

            )

            item["priority"] = round(

                priority,

                2,

            )

            ranked.append(item)

        ranked.sort(

            key=lambda x: x["priority"],

            reverse=True,

        )

        return ranked

    # ---------------------------------------------
    # Long-Term
    # ---------------------------------------------

    @classmethod
    def long_term(
        cls,
        memories,
    ):

        now = time()

        ranked = []

        for memory in memories:

            item = deepcopy(memory)

            score = 0

            score += (

                memory.get(
                    "importance",
                    50,
                )

                * cls.IMPORTANCE_WEIGHT

            )

            if memory.get(

                "pinned",

                False,

            ):

                score += cls.PINNED_WEIGHT

            age = (

                now -

                memory.get(

                    "updated_at",

                    now,

                )

            ) / 3600

            score += max(

                0,

                cls.RECENCY_WEIGHT - age,

            )

            item["priority"] = round(

                score,

                2,

            )

            ranked.append(item)

        ranked.sort(

            key=lambda x: x["priority"],

            reverse=True,

        )

        return ranked

    # ---------------------------------------------
    # Semantic
    # ---------------------------------------------

    @classmethod
    def semantic(
        cls,
        memories,
    ):

        now = time()

        ranked = []

        for memory in memories:

            item = deepcopy(memory)

            score = 0

            score += (

                memory.get(
                    "importance",
                    50,
                )

                * cls.IMPORTANCE_WEIGHT

            )

            age = (

                now -

                memory.get(

                    "created_at",

                    now,

                )

            ) / 3600

            score += max(

                0,

                cls.RECENCY_WEIGHT - age,

            )

            item["priority"] = round(

                score,

                2,

            )

            ranked.append(item)

        ranked.sort(

            key=lambda x: x["priority"],

            reverse=True,

        )

        return ranked

    # ---------------------------------------------
    # Top Context
    # ---------------------------------------------

    @classmethod
    def top(
        cls,
        items,
        limit=10,
    ):

        return deepcopy(

            sorted(

                items,

                key=lambda x: x.get(

                    "priority",

                    0,

                ),

                reverse=True,

            )[:limit]

        )

    # ---------------------------------------------
    # Statistics
    # ---------------------------------------------

    @classmethod
    def statistics(
        cls,
        context,
    ):

        return {

            "conversation": len(

                context.get(

                    "conversation",

                    [],

                )

            ),

            "session": len(

                context.get(

                    "session",

                    [],

                )

            ),

            "long_term": len(

                context.get(

                    "long_term",

                    [],

                )

            ),

            "semantic": len(

                context.get(

                    "semantic",

                    [],

                )

            ),

            "highest_conversation_priority":

                max(

                    [

                        x.get(

                            "priority",

                            0,

                        )

                        for x in context.get(

                            "conversation",

                            [],

                        )

                    ],

                    default=0,

                ),

            "highest_long_term_priority":

                max(

                    [

                        x.get(

                            "priority",

                            0,

                        )

                        for x in context.get(

                            "long_term",

                            [],

                        )

                    ],

                    default=0,

                ),

            "highest_semantic_priority":

                max(

                    [

                        x.get(

                            "priority",

                            0,

                        )

                        for x in context.get(

                            "semantic",

                            [],

                        )

                    ],

                    default=0,

                ),

        }