from typing import List


class ToolRanker:

    SERVER_KEYWORDS = {

        "filesystem": [
            "file",
            "folder",
            "directory",
            "docs",
            "document",
            "read",
            "open",
            "write",
            "edit",
            "search",
            "find",
        ],

        "docker": [
            "docker",
            "container",
            "containers",
            "image",
            "images",
            "volume",
            "network",
            "compose",
            "logs",
            "restart",
            "start",
            "stop",
        ],

        "github": [
            "github",
            "repository",
            "repo",
            "branch",
            "commit",
            "pull request",
            "issue",
            "workflow",
            "actions",
        ],

        "kubernetes": [
            "kubernetes",
            "k8s",
            "pod",
            "pods",
            "deployment",
            "service",
            "namespace",
            "cluster",
            "ingress",
        ],

        "postgres": [
            "database",
            "postgres",
            "postgresql",
            "sql",
            "table",
            "query",
        ],

        "aws": [
            "aws",
            "ec2",
            "s3",
            "lambda",
            "cloudwatch",
            "iam",
            "vpc",
        ],

        "prometheus": [
            "metrics",
            "prometheus",
            "monitor",
            "alerts",
        ],

        "grafana": [
            "grafana",
            "dashboard",
            "visualization",
            "panel",
        ],
    }

    @classmethod
    def rank(
        cls,
        message: str,
        tools: List[dict],
    ):

        message = message.lower()

        scored = []

        for tool in tools:

            server = tool["server"]

            score = 0

            for keyword in cls.SERVER_KEYWORDS.get(server, []):

                if keyword in message:
                    score += 1

            scored.append((score, tool))

        scored.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [tool for _, tool in scored]