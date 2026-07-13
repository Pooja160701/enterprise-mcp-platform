import json


class PromptBuilder:
    """
    Builds prompts for the AI Planner.

    This class keeps prompt engineering separate from the
    planner logic so prompts can evolve without changing
    planner code.
    """

    @staticmethod
    def build_planner_prompt(
        user_message: str,
        tools: list[dict],
    ) -> str:

        tool_list = []

        for tool in tools:

            tool_list.append(
                {
                    "server": tool["server"],
                    "tool": tool["name"],
                    "description": tool.get(
                        "description",
                        "",
                    ),
                }
            )

        return f"""
You are an Enterprise AI Infrastructure Planner.

Your job is NOT to answer the user.

Your job is ONLY to create an execution plan.

Available tools:

{json.dumps(tool_list, indent=2)}

Rules:

1. Always search before reading files.

BAD:
read README.md

GOOD:
search README.md
read README.md

2. Never invent file paths.

3. Never invent repository names.

4. Prefer the smallest number of tools.

5. Multiple tools are allowed when required.

6. If a file path is unknown:

search_files
↓

read_text_file

7. If repository name is unknown:

list_repositories
↓

repository_info

↓

latest_commit

8. Never assume defaults.

9. If one step depends on another, include "depends_on".

10. Return ONLY valid JSON.

11. Do not wrap JSON inside markdown.

id
server
tool
arguments

Example:

[
  {{
    "id": 1,
    "server": "filesystem",
    "tool": "search_files",
    "arguments": {{
      "pattern": "README.md"
    }}
  }},
  {{
    "id": 2,
    "depends_on": 1,
    "server": "filesystem",
    "tool": "read_text_file",
    "arguments": {{
      "path": "$step1.first_match"
    }}
  }}
]

User Request:

{user_message}

Return ONLY JSON.
"""