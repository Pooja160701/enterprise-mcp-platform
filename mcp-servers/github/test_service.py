from service import GitHubService

service = GitHubService()

print()

print("Repositories")

print(service.list_repositories())