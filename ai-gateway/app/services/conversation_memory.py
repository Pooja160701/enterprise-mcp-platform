class ConversationMemory:

    _memory = {}

    @classmethod
    def save(
        cls,
        conversation,
        plan,
        results,
    ):

        cls._memory[conversation] = {

            "plan": plan,

            "results": results,

        }

    @classmethod
    def load(
        cls,
        conversation,
    ):

        return cls._memory.get(
            conversation
        )