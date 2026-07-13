from app.services.memory_service import MemoryService


class ContextService:

    @staticmethod
    def build(

        conversation,

    ):

        memory = MemoryService.conversation(

            conversation

        )

        if not memory:

            return ""

        context = ""

        if "last_message" in memory:

            context += f"""

Previous User Request

{memory["last_message"]}

"""

        if "last_results" in memory:

            context += """

Previous Results

"""

            context += str(

                memory["last_results"]

            )

        return context