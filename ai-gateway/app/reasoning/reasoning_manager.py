from copy import deepcopy

from app.reasoning.reasoning_engine import ReasoningEngine
from app.reasoning.reflection import Reflection
from app.reasoning.self_critique import SelfCritique
from app.reasoning.decision_engine import DecisionEngine
from app.reasoning.reasoning_trace import ReasoningTrace
from app.reasoning.tool_planner import ToolPlanner
from app.reasoning.goal_tracker import GoalTracker


class ReasoningManager:
    """
    Enterprise Reasoning Manager

                  User Query
                       │
                       ▼
               Reasoning Engine
                       │
                       ▼
               Decision Engine
                       │
                       ▼
                 Tool Planner
                       │
                       ▼
                  Reflection
                       │
                       ▼
                 Self Critique
                       │
                       ▼
                Reasoning Trace
                       │
                       ▼
                 Final Reasoning

    Central entry point for all reasoning.
    """

    def __init__(self):

        self.engine = ReasoningEngine()
        self.decision = DecisionEngine()
        self.reflection = Reflection()
        self.critique = SelfCritique()
        self.trace = ReasoningTrace()
        self.planner = ToolPlanner()
        self.goals = GoalTracker()

    # -------------------------------------------------
    # Run Complete Reasoning
    # -------------------------------------------------

    def run(
        self,
        query,
        context=None,
    ):

        context = context or {}

        self.trace.start(query)

        #
        # Step 1 : Reasoning
        #

        self.engine.reason(query)

        self.trace.add_step(
            "reasoning",
            self.engine.export(),
        )

        #
        # Step 2 : Decision
        #

        self.decision.decide(query)

        self.trace.decision(
            self.decision.decision(),
            self.decision.reason(),
        )

        #
        # Step 3 : Tool Planning
        #

        self.planner.clear()

        if self.decision.requires_tool():

            self.planner.add(
                tool="auto.selected.tool",
                priority=100,
                parallel=(
                    self.decision.decision()
                    == DecisionEngine.PARALLEL
                ),
            )

        execution_plan = self.planner.build()

        self.trace.add_step(
            "tool_plan",
            execution_plan,
        )

        #
        # Step 4 : Reflection
        #

        response = "Reasoning completed successfully."

        self.reflection.reflect(
            query,
            response,
        )

        self.trace.reflection(
            self.reflection.export(),
        )

        #
        # Step 5 : Self Critique
        #

        self.critique.critique(
            query,
            response,
        )

        self.trace.critique(
            self.critique.export(),
        )

        #
        # Finish Trace
        #

        self.trace.response(
            response,
        )

        #
        # Final Result
        #

        return {

            "reasoning": self.engine.export(),

            "decision": self.decision.export(),

            "tool_plan": execution_plan,

            "reflection": self.reflection.export(),

            "critique": self.critique.export(),

            "trace": self.trace.export(),

        }

    # -------------------------------------------------
    # Goal Management
    # -------------------------------------------------

    def add_goal(
        self,
        goal,
        priority=50,
        depends_on=None,
    ):

        return self.goals.add(
            goal,
            priority,
            depends_on,
        )

    def complete_goal(
        self,
        goal_id,
    ):

        return self.goals.complete(
            goal_id,
        )

    def goal_statistics(
        self,
    ):

        return self.goals.statistics()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "reasoning_engine": deepcopy(
                self.engine.statistics()
            ),

            "decision_engine": deepcopy(
                self.decision.statistics()
            ),

            "tool_planner": deepcopy(
                self.planner.statistics()
            ),

            "reflection": deepcopy(
                self.reflection.statistics()
            ),

            "self_critique": deepcopy(
                self.critique.statistics()
            ),

            "reasoning_trace": deepcopy(
                self.trace.statistics()
            ),

            "goal_tracker": deepcopy(
                self.goals.statistics()
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self.trace.clear()
        self.planner.clear()
        self.goals.clear()

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "trace": self.trace.export(),

            "goals": self.goals.export(),

            "plan": self.planner.export(),

        }

    # -------------------------------------------------
    # Empty Manager
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ReasoningManager()