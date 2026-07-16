from copy import deepcopy


class DecisionEngine:
    """
    Enterprise Decision Engine

    Determines the next action for the agent.

    Responsibilities

    ✓ Answer Directly
    ✓ Call Tools
    ✓ Execute in Parallel
    ✓ Ask for Clarification
    ✓ Retry Failed Actions
    ✓ Human Approval
    ✓ Stop Execution

    Used by

    - Reasoning Engine
    - Agent Service
    - Workflow Engine
    - Reasoning Manager
    """

    ANSWER = "answer"

    TOOL = "tool"

    PARALLEL = "parallel"

    CLARIFY = "clarify"

    RETRY = "retry"

    HUMAN = "human"

    STOP = "stop"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Decide
    # -------------------------------------------------

    def decide(
        self,
        query,
        reasoning=None,
        reflection=None,
        critique=None,
    ):

        self.clear()

        self._query = query

        text = str(query).lower()

        #
        # Human Approval
        #

        if critique is not None:

            if hasattr(critique, "approved"):

                if not critique.approved():

                    self._decision = self.HUMAN

                    self._reason = "Low confidence requires human approval."

                    return self

        #
        # Retry
        #

        if reflection is not None:

            if hasattr(reflection, "successful"):

                if not reflection.successful():

                    self._decision = self.RETRY

                    self._reason = "Reflection reported unsuccessful execution."

                    return self

        #
        # Clarification
        #

        if len(text.split()) <= 2:

            self._decision = self.CLARIFY

            self._reason = "Insufficient user information."

            return self

        #
        # Parallel Tool Execution
        #

        parallel_keywords = [

            "and",

            "also",

            "together",

            "simultaneously",

            "parallel",

            "both",

        ]

        if any(

            keyword in text

            for keyword in parallel_keywords

        ):

            self._decision = self.PARALLEL

            self._reason = "Multiple operations detected."

            return self

        #
        # Tool Execution
        #

        tool_keywords = [

            "github",

            "filesystem",

            "database",

            "memory",

            "search",

            "tool",

            "file",

            "branch",

            "repository",

            "commit",

        ]

        if any(

            keyword in text

            for keyword in tool_keywords

        ):

            self._decision = self.TOOL

            self._reason = "External tool required."

            return self

        #
        # Direct Answer
        #

        self._decision = self.ANSWER

        self._reason = "LLM can answer directly."

        return self

    # -------------------------------------------------
    # Decision
    # -------------------------------------------------

    def decision(
        self,
    ):

        return self._decision

    # -------------------------------------------------
    # Reason
    # -------------------------------------------------

    def reason(
        self,
    ):

        return self._reason

    # -------------------------------------------------
    # Requires Tool
    # -------------------------------------------------

    def requires_tool(
        self,
    ):

        return self._decision in (

            self.TOOL,

            self.PARALLEL,

        )

    # -------------------------------------------------
    # Requires Human
    # -------------------------------------------------

    def requires_human(
        self,
    ):

        return self._decision == self.HUMAN

    # -------------------------------------------------
    # Retry
    # -------------------------------------------------

    def should_retry(
        self,
    ):

        return self._decision == self.RETRY

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "query": self._query,

            "decision": self._decision,

            "reason": self._reason,

        }

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "decision": self._decision,

            "reason": self._reason,

            "tool_required": self.requires_tool(),

            "human_required": self.requires_human(),

            "retry": self.should_retry(),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._query = ""

        self._decision = self.ANSWER

        self._reason = ""

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return DecisionEngine()