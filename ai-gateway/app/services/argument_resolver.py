class ArgumentResolver:

    @staticmethod
    def resolve(tool: str, arguments: dict):

        if tool == "list_directory":

            path = arguments.get("path", "").strip()

            if path in ("docs", "/docs", "doc"):

                arguments["path"] = "/app/docs"

        return arguments