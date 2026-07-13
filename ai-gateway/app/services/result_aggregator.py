class ResultAggregator:
    """
    Converts MCP execution results into a single
    text block for the LLM.
    """

    @staticmethod
    def aggregate(results: list) -> str:

        sections = []

        for item in results:

            server = item["server"]
            tool = item["tool"]
            result = item["result"]

            text = ""

            #
            # MCP Response
            #
            if hasattr(result, "content") and result.content:

                blocks = []

                for block in result.content:

                    if hasattr(block, "text"):

                        blocks.append(block.text)

                text = "\n".join(blocks)

            #
            # Plain Python response
            #
            else:

                text = str(result)

            sections.append(
                "\n".join(
                    [
                        "=" * 60,
                        f"SERVER : {server}",
                        f"TOOL   : {tool}",
                        "=" * 60,
                        text.strip(),
                    ]
                )
            )

        return "\n\n".join(sections)