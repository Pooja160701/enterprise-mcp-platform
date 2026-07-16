import time
from copy import deepcopy


class ReasoningTrace:
    """
    Enterprise Reasoning Trace

    Records every reasoning step performed by the agent.

    Features

    ✓ Thought Trace
    ✓ Decisions
    ✓ Tool Calls
    ✓ Tool Results
    ✓ Reflection
    ✓ Self Critique
    ✓ Timing
    ✓ Statistics

    Used by

    - Reasoning Engine
    - Agent Service
    - Workflow Engine
    - Observability
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Start
    # -------------------------------------------------

    def start(
        self,
        query,
    ):

        self.clear()

        self._query = query

        self._started = time.time()

        return self

    # -------------------------------------------------
    # Add Step
    # -------------------------------------------------

    def add_step(
        self,
        name,
        data=None,
    ):

        self._steps.append(

            {

                "timestamp": time.time(),

                "step": name,

                "data": deepcopy(data),

            }

        )

        return self

    # -------------------------------------------------
    # Decision
    # -------------------------------------------------

    def decision(
        self,
        decision,
        reason=None,
    ):

        self._decision = {

            "decision": decision,

            "reason": reason,

            "timestamp": time.time(),

        }

        return self

    # -------------------------------------------------
    # Tool Call
    # -------------------------------------------------

    def tool_call(
        self,
        tool,
        arguments=None,
    ):

        self._tool_calls.append(

            {

                "tool": tool,

                "arguments": deepcopy(arguments),

                "timestamp": time.time(),

            }

        )

        return self

    # -------------------------------------------------
    # Tool Result
    # -------------------------------------------------

    def tool_result(
        self,
        tool,
        result,
    ):

        self._tool_results.append(

            {

                "tool": tool,

                "result": deepcopy(result),

                "timestamp": time.time(),

            }

        )

        return self

    # -------------------------------------------------
    # Reflection
    # -------------------------------------------------

    def reflection(
        self,
        reflection,
    ):

        self._reflection = deepcopy(reflection)

        return self

    # -------------------------------------------------
    # Critique
    # -------------------------------------------------

    def critique(
        self,
        critique,
    ):

        self._critique = deepcopy(critique)

        return self

    # -------------------------------------------------
    # Final Response
    # -------------------------------------------------

    def response(
        self,
        response,
    ):

        self._response = response

        self._finished = time.time()

        return self

    # -------------------------------------------------
    # Duration
    # -------------------------------------------------

    def duration(
        self,
    ):

        if self._finished is None:

            return round(

                time.time() - self._started,

                3,

            )

        return round(

            self._finished - self._started,

            3,

        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "query": self._query,

            "decision": deepcopy(

                self._decision,

            ),

            "steps": deepcopy(

                self._steps,

            ),

            "tool_calls": deepcopy(

                self._tool_calls,

            ),

            "tool_results": deepcopy(

                self._tool_results,

            ),

            "reflection": deepcopy(

                self._reflection,

            ),

            "critique": deepcopy(

                self._critique,

            ),

            "response": self._response,

            "duration": self.duration(),

        }

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "steps": len(

                self._steps,

            ),

            "tool_calls": len(

                self._tool_calls,

            ),

            "tool_results": len(

                self._tool_results,

            ),

            "has_reflection": self._reflection is not None,

            "has_critique": self._critique is not None,

            "duration": self.duration(),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._query = ""

        self._steps = []

        self._decision = None

        self._tool_calls = []

        self._tool_results = []

        self._reflection = None

        self._critique = None

        self._response = None

        self._started = time.time()

        self._finished = None

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ReasoningTrace()