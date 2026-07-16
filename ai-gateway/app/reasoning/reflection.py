from copy import deepcopy


class Reflection:
    """
    Enterprise Reflection Engine

    Evaluates the reasoning and execution results.

    Responsibilities

    ✓ Validate reasoning
    ✓ Detect incomplete answers
    ✓ Detect failures
    ✓ Suggest improvements
    ✓ Produce reflection summary

    Used by

    - Reasoning Engine
    - Reasoning Manager
    - Agent Service
    """

    def __init__(self):

        self._query = ""

        self._response = ""

        self._observations = []

        self._suggestions = []

        self._successful = False

    # -------------------------------------------------
    # Reflect
    # -------------------------------------------------

    def reflect(
        self,
        query,
        response,
    ):

        self.clear()

        self._query = query

        self._response = response

        if response and len(str(response).strip()) > 0:

            self._successful = True

            self._observations.append(
                "Response generated successfully."
            )

        else:

            self._successful = False

            self._observations.append(
                "Response is empty."
            )

            self._suggestions.append(
                "Generate a more complete response."
            )

        if "error" in str(response).lower():

            self._successful = False

            self._observations.append(
                "Execution reported an error."
            )

            self._suggestions.append(
                "Retry tool execution or request clarification."
            )

        return self

    # -------------------------------------------------
    # Query
    # -------------------------------------------------

    def query(
        self,
    ):

        return self._query

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

    def response(
        self,
    ):

        return self._response

    # -------------------------------------------------
    # Observations
    # -------------------------------------------------

    def observations(
        self,
    ):

        return deepcopy(
            self._observations
        )

    # -------------------------------------------------
    # Suggestions
    # -------------------------------------------------

    def suggestions(
        self,
    ):

        return deepcopy(
            self._suggestions
        )

    # -------------------------------------------------
    # Successful
    # -------------------------------------------------

    def successful(
        self,
    ):

        return self._successful

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "observations": len(
                self._observations
            ),

            "suggestions": len(
                self._suggestions
            ),

            "successful": self._successful,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "query": self._query,

            "response": self._response,

            "observations": deepcopy(
                self._observations
            ),

            "suggestions": deepcopy(
                self._suggestions
            ),

            "successful": self._successful,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._query = ""

        self._response = ""

        self._observations.clear()

        self._suggestions.clear()

        self._successful = False

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return Reflection()