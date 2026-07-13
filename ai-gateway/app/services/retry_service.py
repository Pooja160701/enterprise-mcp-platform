class RetryService:

    @staticmethod
    def should_retry(result):

        text = str(result).lower()

        errors = [

            "not found",

            "404",

            "missing",

            "cannot find",

            "no such file",

        ]

        return any(e in text for e in errors)