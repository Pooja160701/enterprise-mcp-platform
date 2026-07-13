import docker

client = docker.from_env()

print("Docker version:")
print(client.version())

print("\nRunning containers:")
print(client.containers.list())

print("\nAll containers:")
print(client.containers.list(all=True))