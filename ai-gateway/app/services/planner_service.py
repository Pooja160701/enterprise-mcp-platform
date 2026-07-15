import json

from app.services.openai_service import OpenAIService

from app.planner.planner_validator import PlannerValidator
from app.planner.plan_repair import PlanRepair
from app.planner.cost_optimizer import CostOptimizer
from app.planner.confidence_scorer import ConfidenceScorer


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

4. If a step depends on another step include

"depends_on":[step_id]

5. If the user already provides an argument
(repository, namespace, pod, deployment,
container, bucket, dashboard, cluster, etc.)

USE THAT VALUE DIRECTLY.

Example

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

Do NOT first call list_repositories.

6. Use placeholders ONLY when a previous step
actually generates the value.

Allowed

$1.name
$1.repository
$1.namespace
$1.bucket
$1.cluster

NOT

$1.repositories[0]
$1.data.results
JMESPath
JSONPath

7. Use the minimum number of tools.

8. Never call discovery tools unless required.

User Request:

{user_message}
"""

        response = await self.llm.chat(prompt)

        print("\nPlanner Raw Response\n")
        print(response)

        #
        # -----------------------------
        # Parse JSON
        # -----------------------------
        #

        plan = self.extract_json(response)

        print("\nPlanner Parsed Plan\n")
        print(json.dumps(plan, indent=2))

        #
        # -----------------------------
        # Validate
        # -----------------------------
        #

        validation = PlannerValidator.validate(
            plan=plan,
            candidate_tools=candidate_tools,
        )

        print("\nPlanner Validation\n")
        print(json.dumps(validation, indent=2))

        #
        # -----------------------------
        # Repair
        # -----------------------------
        #

        repaired = PlanRepair.repair(
            plan=validation["plan"],
            candidate_tools=candidate_tools,
        )

        print("\nPlanner Repair\n")
        print(json.dumps(repaired, indent=2))

        #
        # -----------------------------
        # Optimize
        # -----------------------------
        #

        optimized = CostOptimizer.optimize(
            repaired["plan"]
        )

        print("\nPlanner Optimization\n")
        print(json.dumps(optimized, indent=2))

        #
        # -----------------------------
        # Confidence
        # -----------------------------
        #

        confidence = ConfidenceScorer.score(
            plan=optimized["plan"],
            candidate_tools=candidate_tools,
            repairs=repaired["repairs"],
            optimizations=optimized["optimizations"],
        )

        print("\nPlanner Confidence\n")
        print(json.dumps(confidence, indent=2))

        #
        # -----------------------------
        # Final Result
        # -----------------------------
        #

        return {

            "plan": optimized["plan"],

            "confidence": confidence,

            "validation": validation,

            "repairs": repaired["repairs"],

            "optimizations": optimized["optimizations"],

            "estimated_cost": optimized["estimated_cost"],

        }

    def extract_json(
        self,
        response: str,
    ):

        if not response:

            return []

        response = (

            response

            .replace(
                "```json",
                "",
            )

            .replace(
                "```",
                "",
            )

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

        parsed = []

        for step in plan:

            if not isinstance(
                step,
                dict,
            ):
                continue

            if (
                "server" not in step
                or
                "tool" not in step
            ):
                continue

            parsed.append(

                {

                    "id": step.get(
                        "id",
                        len(parsed) + 1,
                    ),

                    "server": step["server"],

                    "tool": step["tool"],

                    "arguments": (

                        step.get(
                            "arguments",
                            {},
                        )

                        if isinstance(
                            step.get(
                                "arguments",
                                {},
                            ),
                            dict,
                        )

                        else {}

                    ),

                    "depends_on": (

                        step.get(
                            "depends_on",
                            [],
                        )

                        if isinstance(
                            step.get(
                                "depends_on",
                                [],
                            ),
                            list,
                        )

                        else []

                    ),

                }

            )

        return parsed