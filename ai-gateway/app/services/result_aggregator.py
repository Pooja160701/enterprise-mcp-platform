from typing import Any


class ResultAggregator:
    """
    Converts raw MCP tool outputs into a normalized structure
    that the LLM (or UI) can easily consume.
    """

    @staticmethod
    def aggregate(results):

        prompt = ResultAggregator.to_prompt(results)

        return {
            "prompt": prompt,
            "results": results,
        }


    @staticmethod
    def to_prompt(results: list[dict]) -> str:

        lines = []

        for result in results:

            server = result["server"]
            tool = result["tool"]
            data = result["result"]

            lines.append(f"Server: {server}")
            lines.append(f"Tool: {tool}")

            #
            # Filesystem
            #

            if server == "filesystem":

                if tool == "list_directory":

                    if not data:
                        lines.append("No files found.")

                    else:
                        lines.append("Files:")

                        for file in data:
                            if isinstance(file, dict):
                                lines.append(f"- {file.get('name')}")
                            else:
                                lines.append(f"- {file}")

                elif tool == "read_text_file":

                    lines.append(str(data))

            #
            # Docker
            #

            elif server == "docker":

                if isinstance(data, list):

                    lines.append(f"Containers found: {len(data)}")

                    for container in data:

                        lines.append(
                            f"- {container.get('name')} ({container.get('status')})"
                        )

            #
            # Kubernetes
            #

            elif server == "kubernetes":

                if tool == "list_nodes":

                    lines.append(f"Nodes: {len(data)}")

                    for node in data:

                        lines.append(
                            f"- {node['name']} | {node['status']} | {node['kubelet_version']}"
                        )

                elif tool == "list_namespaces":

                    lines.append(f"Namespaces: {len(data)}")

                    for ns in data:

                        lines.append(
                            f"- {ns['name']} ({ns['status']})"
                        )

                else:

                    lines.append(str(data))

            #
            # PostgreSQL
            #

            elif server == "postgres":

                #
                # Normalize
                #

                if isinstance(data, dict):
                    data = [data]

                elif data is None:
                    data = []

                #
                # -----------------------
                # Databases
                # -----------------------
                #

                if tool == "list_databases_tool":

                    lines.append(f"Databases: {len(data)}")

                    for db in data:

                        if isinstance(db, dict):

                            lines.append(
                                f"- {db.get('name', 'Unknown')}"
                            )

                        else:

                            lines.append(f"- {db}")

                #
                # -----------------------
                # Tables
                # -----------------------
                #

                elif tool == "list_tables_tool":

                    if not data:

                        lines.append("Database: enterprise_mcp")
                        lines.append("Schema: public")
                        lines.append("No tables exist.")

                    else:

                        lines.append(f"Tables: {len(data)}")

                        for table in data:

                            if isinstance(table, dict):

                                lines.append(
                                    f"- {table.get('name', 'Unknown')}"
                                )

                            else:

                                lines.append(f"- {table}")

                #
                # -----------------------
                # Describe Table
                # -----------------------
                #

                elif tool == "describe_table_tool":

                    if not data:

                        lines.append("Table not found.")

                    else:

                        for column in data:

                            if isinstance(column, dict):

                                lines.append(
                                    f"- {column.get('column')} | "
                                    f"{column.get('type')} | "
                                    f"Nullable: {column.get('nullable')}"
                                )

                #
                # -----------------------
                # Database Size
                # -----------------------
                #

                elif tool == "database_size_tool":

                    if isinstance(data, dict):

                        lines.append(
                            f"Database Size: {data.get('pretty')} "
                            f"({data.get('bytes')} bytes)"
                        )

                    else:

                        lines.append(str(data))

                #
                # -----------------------
                # Row Count
                # -----------------------
                #

                elif tool == "table_row_count_tool":

                    lines.append(str(data))

                #
                # -----------------------
                # SELECT
                # -----------------------
                #

                elif tool == "run_select_query_tool":

                    if isinstance(data, list):

                        lines.append(f"Rows: {len(data)}")

                        for row in data:

                            lines.append(str(row))

                    else:

                        lines.append(str(data))

                else:

                    lines.append(str(data))

            #
            # GitHub
            #

            elif server == "github":

                if isinstance(data, list):

                    lines.append(
                        f"Repositories: {len(data)}"
                    )

                    for repo in data:

                        lines.append(
                            f"- {repo.get('name')}"
                        )

                else:

                    lines.append(str(data))

            else:

                lines.append(str(data))

            lines.append("")

        return "\n".join(lines)