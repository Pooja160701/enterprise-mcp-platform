from copy import deepcopy


class SelfCritique:
    """
    Enterprise Self Critique

    Reviews the generated reasoning and response before
    returning the final answer.

    Responsibilities

    ✓ Detect hallucinations
    ✓ Detect missing information
    ✓ Detect inconsistencies
    ✓ Evaluate confidence
    ✓ Generate improvement suggestions

    Used by

    - Reasoning Engine
    - Reflection
    - Reasoning Manager
    """

    def __init__(self):

        self._query = ""

        self._response = ""

        self._issues = []

        self._recommendations = []

        self._confidence = 100

        self._approved = True

    # -------------------------------------------------
    # Critique
    # -------------------------------------------------

    def critique(
        self,
        query,
        response,
    ):

        self.clear()

        self._query = query

        self._response = response

        response_text = str(response).strip()

        #
        # Empty Response
        #

        if not response_text:

            self._issues.append(
                "Empty response."
            )

            self._recommendations.append(
                "Generate a complete response."
            )

            self._confidence = 0

            self._approved = False

            return self

        #
        # Error Detection
        #

        if "error" in response_text.lower():

            self._issues.append(
                "Execution error detected."
            )

            self._recommendations.append(
                "Retry execution or use another tool."
            )

            self._confidence -= 40

            self._approved = False

        #
        # Uncertainty Detection
        #

        uncertain = [

            "maybe",

            "possibly",

            "might",

            "not sure",

            "uncertain",

            "guess",

        ]

        if any(

            word in response_text.lower()

            for word in uncertain

        ):

            self._issues.append(
                "Low-confidence language detected."
            )

            self._recommendations.append(
                "Verify information before responding."
            )

            self._confidence -= 20

        #
        # Short Response
        #

        if len(response_text.split()) < 5:

            self._issues.append(
                "Response may be incomplete."
            )

            self._recommendations.append(
                "Provide additional details."
            )

            self._confidence -= 10

        #
        # Confidence Bounds
        #

        self._confidence = max(
            0,
            min(
                100,
                self._confidence,
            ),
        )

        if self._confidence < 60:

            self._approved = False

        return self

    # -------------------------------------------------
    # Approved
    # -------------------------------------------------

    def approved(
        self,
    ):

        return self._approved

    # -------------------------------------------------
    # Confidence
    # -------------------------------------------------

    def confidence(
        self,
    ):

        return self._confidence

    # -------------------------------------------------
    # Issues
    # -------------------------------------------------

    def issues(
        self,
    ):

        return deepcopy(
            self._issues
        )

    # -------------------------------------------------
    # Recommendations
    # -------------------------------------------------

    def recommendations(
        self,
    ):

        return deepcopy(
            self._recommendations
        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "issues": len(
                self._issues
            ),

            "recommendations": len(
                self._recommendations
            ),

            "confidence": self._confidence,

            "approved": self._approved,

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

            "issues": deepcopy(
                self._issues
            ),

            "recommendations": deepcopy(
                self._recommendations
            ),

            "confidence": self._confidence,

            "approved": self._approved,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._query = ""

        self._response = ""

        self._issues.clear()

        self._recommendations.clear()

        self._confidence = 100

        self._approved = True

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return SelfCritique()