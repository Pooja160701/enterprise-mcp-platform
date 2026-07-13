from app.services.tool_ranker import ToolRanker


class ToolSelector:

    @staticmethod
    def select(
        message: str,
        tools: list,
    ):

        ranked = ToolRanker.rank(
            message,
            tools,
        )

        return ranked[:5]