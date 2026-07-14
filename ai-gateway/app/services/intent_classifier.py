import re


class IntentClassifier:
    """
    Fast rule-based intent classifier.

    Returns:
        dict | None

    Example:

    {
        "server": "postgres",
        "tool": "list_tables_tool",
        "arguments": {
            "schema": "public"
        }
    }
    """

    @staticmethod
    def classify(message: str):

        text = message.lower().strip()

        #
        # Filesystem
        #

        if re.search(r"list.*docs|list.*files", text):
            return {
                "server": "filesystem",
                "tool": "list_directory",
                "arguments": {
                    "path": "docs"
                }
            }

        #
        # Kubernetes
        #

        if "nodes" in text:
            return {
                "server": "kubernetes",
                "tool": "list_nodes",
                "arguments": {}
            }

        if "namespaces" in text:
            return {
                "server": "kubernetes",
                "tool": "list_namespaces",
                "arguments": {}
            }

        if "pods" in text:
            return {
                "server": "kubernetes",
                "tool": "list_pods",
                "arguments": {}
            }

        if "deployments" in text:
            return {
                "server": "kubernetes",
                "tool": "list_deployments",
                "arguments": {}
            }

        if "services" in text:
            return {
                "server": "kubernetes",
                "tool": "list_services",
                "arguments": {}
            }

        #
        # Docker
        #

        if "running containers" in text:
            return {
                "server": "docker",
                "tool": "list_running_containers",
                "arguments": {}
            }

        if "images" in text:
            return {
                "server": "docker",
                "tool": "list_images",
                "arguments": {}
            }

        #
        # PostgreSQL
        #

        if "database size" in text:
            return {
                "server": "postgres",
                "tool": "database_size_tool",
                "arguments": {}
            }

        if "list databases" in text or "show databases" in text:
            return {
                "server": "postgres",
                "tool": "list_databases_tool",
                "arguments": {}
            }

        if "list tables" in text or "show tables" in text:
            return {
                "server": "postgres",
                "tool": "list_tables_tool",
                "arguments": {
                    "schema": "public"
                }
            }

        #
        # GitHub
        #

        if "repositories" in text:
            return {
                "server": "github",
                "tool": "list_repositories",
                "arguments": {}
            }

        return None