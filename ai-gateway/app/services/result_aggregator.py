class ResultAggregator:

    @staticmethod
    def aggregate(results):

        sections = []

        for item in results:

            result = item["result"]

            text = ""

            if hasattr(result, "content"):

                text = "\n".join(

                    block.text

                    for block in result.content

                    if hasattr(block, "text")

                )

            else:

                text = str(result)

            sections.append({

                "server": item["server"],

                "tool": item["tool"],

                "output": text,

            })

        return sections

    @staticmethod
    def to_prompt(results):

        prompt = ""

        for item in results:

            prompt += f"""

Server:
{item["server"]}

Tool:
{item["tool"]}

Output:

{item["output"]}

"""

        return prompt