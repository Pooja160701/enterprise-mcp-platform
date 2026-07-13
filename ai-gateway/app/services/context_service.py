class ContextService:
    """
    Extracts reusable context from tool execution results.
    """

    @staticmethod
    def update(memory, step, result):

        tool = step["tool"]

        #
        # GitHub
        #

        if tool == "list_repositories":

            if isinstance(result, list) and result:

                memory["repository"] = result[0]["full_name"]

        #
        # Filesystem
        #

        elif tool == "search_files":

            if isinstance(result, dict):

                first = result.get("first_match")

                if first:

                    memory["last_file"] = first

        elif tool == "read_text_file":

            path = step["arguments"].get("path")

            if path:

                memory["last_file"] = path

        #
        # Docker
        #

        elif tool == "list_running_containers":

            if isinstance(result, list) and result:

                memory["container"] = result[0]["name"]

        elif tool in {

            "start_container",

            "stop_container",

            "container_logs",

        }:

            name = step["arguments"].get("name")

            if name:

                memory["container"] = name

        return memory