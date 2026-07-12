from app.services.agent_service import AgentService


class AIService:

    def __init__(self):

        self.agent = AgentService()

    async def chat(self, message: str):

        return await self.agent.chat(message)