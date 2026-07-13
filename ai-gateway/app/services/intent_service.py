from app.services.openai_service import OpenAIService
from app.services.intent_parser import IntentParser


class IntentService:
    """
    Detects which MCP servers are relevant
    for the user's request.
    """

    SERVERS = [
        "filesystem",
        "docker",
        "github",
        "kubernetes",
        "postgres",
        "prometheus",
        "grafana",
        "aws",
    ]

    def __init__(self):
        self.openai = OpenAIService()

    async def detect(self, message: str):

        prompt = f"""
You are an intent classifier.

Available servers:

{", ".join(self.SERVERS)}

User request:

{message}

Return ONLY a JSON array.

Example:

["filesystem"]

or

["github","docker"]

Do not explain.
"""

        response = await self.openai.chat(prompt)

        return IntentParser.parse(response)