class ArgumentResolver:

    @staticmethod
    def resolve(
        tool: str,
        arguments: dict,
    ):

        if arguments is None:
            arguments = {}

        #
        # Filesystem tools
        #

        if tool == "list_directory":
            arguments.setdefault("path", "/app/docs")

        elif tool == "directory_tree":
            arguments.setdefault("path", "/app/docs")

        elif tool == "search_files":
            arguments.setdefault("path", "/app/docs")

        elif tool == "read_text_file":
            arguments.setdefault("head", 200)

        #
        # Docker tools
        #

        elif tool in (
            "inspect_container",
            "start_container",
            "stop_container",
            "container_logs",
        ):

            #
            # GPT may return:
            #
            # container
            # container_name
            # name
            #

            if "name" not in arguments:

                if "container" in arguments:
                    arguments["name"] = arguments.pop("container")

                elif "container_name" in arguments:
                    arguments["name"] = arguments.pop("container_name")

        if tool == "container_logs":
            arguments.setdefault("tail", 50)

        return arguments