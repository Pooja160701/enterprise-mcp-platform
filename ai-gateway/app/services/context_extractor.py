import re


class ContextExtractor:

    @staticmethod
    def extract(
        message: str,
    ):

        context = {}

        #
        # GitHub repository
        #

        repo = re.search(
            r"repository\s+([A-Za-z0-9._-]+)",
            message,
            re.I,
        )

        if repo:
            context["repository"] = repo.group(1)

        #
        # PostgreSQL table
        #

        table = re.search(
            r"table\s+([A-Za-z0-9_]+)",
            message,
            re.I,
        )

        if table:
            context["table"] = table.group(1)

        #
        # File
        #

        file = re.search(
            r"([A-Za-z0-9._-]+\.(md|txt|py|json|yaml|yml))",
            message,
            re.I,
        )

        if file:
            context["file"] = file.group(1)

        return context