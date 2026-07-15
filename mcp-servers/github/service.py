from pathlib import Path
import os

from dotenv import load_dotenv
from github import Github

load_dotenv(Path("/") / ".env")


class GitHubService:

    def __init__(self):

        token = (
            os.getenv("GITHUB_TOKEN")
            or os.getenv("GITHUB_PAT")
        )

        if not token:
            raise RuntimeError(
                "GITHUB_TOKEN environment variable not found."
            )

        self.client = Github(token)

        #
        # Default owner
        #
        self.owner = (
            os.getenv("GITHUB_OWNER")
            or self.client.get_user().login
        )

    #
    # -----------------------------------------
    # Helpers
    # -----------------------------------------
    #

    def get_repo(self, repository: str):

        #
        # Allow either:
        #
        # enterprise-mcp-platform
        #
        # or
        #
        # Pooja160701/enterprise-mcp-platform
        #

        if "/" not in repository:

            repository = f"{self.owner}/{repository}"

        return self.client.get_repo(repository)

    #
    # -----------------------------------------
    # Repositories
    # -----------------------------------------
    #

    def list_repositories(self):

        repos = []

        for repo in self.client.get_user().get_repos():

            repos.append(
                {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "private": repo.private,
                    "default_branch": repo.default_branch,
                    "url": repo.html_url,
                }
            )

        return repos

    def repository_info(
        self,
        repository: str,
    ):

        repo = self.get_repo(repository)

        return {

            "name": repo.name,

            "full_name": repo.full_name,

            "description": repo.description,

            "stars": repo.stargazers_count,

            "forks": repo.forks_count,

            "watchers": repo.watchers_count,

            "language": repo.language,

            "default_branch": repo.default_branch,

            "url": repo.html_url,

        }

    #
    # -----------------------------------------
    # Branches
    # -----------------------------------------
    #

    def list_branches(
        self,
        repository: str,
    ):

        repo = self.get_repo(repository)

        branches = []

        for branch in repo.get_branches():

            branches.append(
                {
                    "name": branch.name,
                }
            )

        return branches

    #
    # -----------------------------------------
    # Commits
    # -----------------------------------------
    #

    def latest_commit(
        self,
        repository: str,
    ):

        repo = self.get_repo(repository)

        commit = repo.get_commits()[0]

        return {

            "sha": commit.sha,

            "author": commit.commit.author.name,

            "message": commit.commit.message,

            "date": str(commit.commit.author.date),

        }

    #
    # -----------------------------------------
    # Issues
    # -----------------------------------------
    #

    def list_issues(
        self,
        repository: str,
    ):

        repo = self.get_repo(repository)

        issues = []

        for issue in repo.get_issues(state="open"):

            if issue.pull_request:
                continue

            issues.append(
                {
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                }
            )

        return issues

    def create_issue(
        self,
        repository: str,
        title: str,
        body: str = "",
    ):

        repo = self.get_repo(repository)

        issue = repo.create_issue(
            title=title,
            body=body,
        )

        return {

            "number": issue.number,

            "title": issue.title,

            "url": issue.html_url,

        }

    def close_issue(
        self,
        repository: str,
        issue_number: int,
    ):

        repo = self.get_repo(repository)

        issue = repo.get_issue(issue_number)

        issue.edit(state="closed")

        return {

            "number": issue.number,

            "status": "closed",

        }

    #
    # -----------------------------------------
    # Pull Requests
    # -----------------------------------------
    #

    def list_pull_requests(
        self,
        repository: str,
    ):

        repo = self.get_repo(repository)

        pulls = []

        for pr in repo.get_pulls():

            pulls.append(
                {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                }
            )

        return pulls

    #
    # -----------------------------------------
    # Workflows
    # -----------------------------------------
    #

    def list_workflows(
        self,
        repository: str,
    ):

        repo = self.get_repo(repository)

        workflows = repo.get_workflows()

        result = []

        for workflow in workflows:

            result.append(
                {
                    "name": workflow.name,
                    "id": workflow.id,
                    "state": workflow.state,
                }
            )

        return result