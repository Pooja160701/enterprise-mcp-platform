from typing import List


class ToolRanker:

    KEYWORDS = {

        "list_directory": [
            "list",
            "files",
            "folder",
            "directory",
            "docs",
            "show files",
        ],

        "directory_tree": [
            "tree",
            "structure",
            "hierarchy",
        ],

        "read_text_file": [
            "read",
            "open",
            "show",
            "display",
            "content",
            "file",
        ],

        "search_files": [
            "find",
            "search",
            "locate",
        ],

        "write_file": [
            "write",
            "create",
            "save",
        ],

        "edit_file": [
            "edit",
            "modify",
            "update",
        ],

    }

    @classmethod
    def rank(
        cls,
        message: str,
        tools: List[dict],
    ):

        message = message.lower()

        scores = []

        for tool in tools:

            score = 0

            for keyword in cls.KEYWORDS.get(tool["name"], []):

                if keyword in message:

                    score += 1

            scores.append(
                (
                    score,
                    tool,
                )
            )

        scores.sort(
            reverse=True,
            key=lambda x: x[0],
        )

        return [

            tool

            for _, tool in scores

        ]