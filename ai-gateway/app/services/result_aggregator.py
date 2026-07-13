import json


class ResultAggregator:
    """
    Aggregates MCP execution results.

    Produces:
      - structured data for memory/UI
      - prompt text for the LLM
    """

    @staticmethod
    def aggregate(results: list) -> dict:

        sections = []

        prompt_parts = []

        for item in results:

            server = item["server"]
            tool = item["tool"]
            result = item["result"]

            #
            # MCP Content Blocks
            #
            if hasattr(result, "content") and result.content:

                text = "\n".join(
                    block.text
                    for block in result.content
                    if hasattr(block, "text")
                )

            #
            # dict / list
            #
            elif isinstance(result, (dict, list)):

                text = json.dumps(
                    result,
                    indent=2,
                )

            #
            # everything else
            #
            else:

                text = str(result)

            sections.append(
                {
                    "server": server,
                    "tool": tool,
                    "text": text,
                }
            )

            prompt_parts.append(
                f"""=== {server} :: {tool} ===

{text}
"""
            )

        return {

            "sections": sections,

            "prompt": "\n".join(prompt_parts),

        }

    @staticmethod
    def to_prompt(results: list) -> str:
        """
        Backward compatibility.
        """

        return ResultAggregator.aggregate(results)["prompt"]