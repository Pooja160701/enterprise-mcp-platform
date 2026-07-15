import json

from app.services.openai_service import OpenAIService


class PlannerService:

    def __init__(self):
        self.llm = OpenAIService()

    async def create_plan(
        self,
        user_message: str,
        candidate_tools,
    ):

        prompt = f"""
You are an Enterprise MCP Planner.

Available tools:

{json.dumps(candidate_tools, indent=2)}

Your job is to generate the SMALLEST executable tool plan.

Return ONLY valid JSON.

Rules

1. Return ONLY a JSON array.

2. Do NOT use markdown.

3. Every step MUST contain

{{
    "id": integer,
    "server": "...",
    "tool": "...",
    "arguments": {{}}
}}

4. If a step depends on another step, include

"depends_on":[step_id]

5. If the user already provides an argument
(repository name, namespace, pod, deployment,
container, bucket, cluster, dashboard, etc.)
USE THAT VALUE DIRECTLY.

Example

User:
Show branches for enterprise-mcp-platform

Correct

[
    {{
        "id":1,
        "server":"github",
        "tool":"list_branches",
        "arguments":{{
            "repository":"enterprise-mcp-platform"
        }}
    }}
]

Wrong

list_repositories

↓

list_branches("$1.repositories[...]")

6. Only use placeholders when the value truly
comes from a previous tool.

Allowed placeholders

$1.name
$1.repository
$1.namespace
$1.bucket
$1.cluster
$1.container
$1.dashboard

Do NOT generate expressions such as

$1.repositories[...]
$1.items[0]
$1.data.results
$1.foo.bar[0]
JMESPath
JSONPath
or any array filtering syntax.

7. Use the minimum number of tools.

8. Never call discovery tools unless required.

Examples

User:
List GitHub repositories

↓

[
    {{
        "id":1,
        "server":"github",
        "tool":"list_repositories",
        "arguments":{{}}
    }}
]

--------------------------------------------

User:
Show branches for enterprise-mcp-platform

↓

[
    {{
        "id":1,
        "server":"github",
        "tool":"list_branches",
        "arguments":{{
            "repository":"enterprise-mcp-platform"
        }}
    }}
]

--------------------------------------------

User:
Show latest commit for enterprise-mcp-platform

↓

[
    {{
        "id":1,
        "server":"github",
        "tool":"latest_commit",
        "arguments":{{
            "repository":"enterprise-mcp-platform"
        }}
    }}
]

--------------------------------------------

User:
List Kubernetes pods in kube-system

↓

[
    {{
        "id":1,
        "server":"kubernetes",
        "tool":"list_pods",
        "arguments":{{
            "namespace":"kube-system"
        }}
    }}
]

--------------------------------------------

User:
Show Prometheus targets

↓

[
    {{
        "id":1,
        "server":"prometheus",
        "tool":"list_targets_tool",
        "arguments":{{}}
    }}
]

--------------------------------------------

Only return JSON.

User Request:

{user_message}
"""

        response = await self.llm.chat(prompt)

        print("\nPlanner Raw Response\n")
        print(response)

        plan = self.extract_json(response)

        print("\nPlanner Parsed Plan\n")
        print(json.dumps(plan, indent=2))

        return plan

    def extract_json(
        self,
        response: str,
    ):

        if not response:
            return []

        response = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        start = response.find("[")

        end = response.rfind("]")

        if start == -1 or end == -1:
            return []

        try:
            plan = json.loads(
                response[start:end + 1]
            )

        except Exception as e:

            print(
                f"Planner JSON parse error: {e}"
            )

            return []

        validated = []

        for step in plan:

            if not isinstance(step, dict):
                continue

            if (
                "server" not in step
                or "tool" not in step
            ):
                continue

            arguments = step.get("arguments", {})

            if not isinstance(arguments, dict):
                arguments = {}

            depends = step.get(
                "depends_on",
                [],
            )

            if not isinstance(depends, list):
                depends = []

            validated.append(
                {
                    "id": step.get(
                        "id",
                        len(validated) + 1,
                    ),
                    "server": step["server"],
                    "tool": step["tool"],
                    "arguments": arguments,
                    "depends_on": depends,
                }
            )

        return validated