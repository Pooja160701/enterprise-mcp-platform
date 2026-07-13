class IntentService:

    FILESYSTEM = "filesystem"
    DOCKER = "docker"
    GITHUB = "github"
    GENERAL = "general"

    @classmethod
    def detect(cls, message: str):

        message = message.lower()

        docker = [
            "container",
            "docker",
            "image",
            "logs",
            "restart",
            "stop",
            "start",
        ]

        github = [
            "repository",
            "repo",
            "github",
            "branch",
            "commit",
            "issue",
            "workflow",
            "pull request",
        ]

        filesystem = [
            "file",
            "folder",
            "directory",
            "read",
            "write",
            "create",
            "edit",
            "search",
        ]

        if any(word in message for word in docker):
            return cls.DOCKER

        if any(word in message for word in github):
            return cls.GITHUB

        if any(word in message for word in filesystem):
            return cls.FILESYSTEM

        return cls.GENERAL