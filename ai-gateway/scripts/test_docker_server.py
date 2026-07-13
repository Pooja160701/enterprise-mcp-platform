from core.servers.docker.service import DockerService

service = DockerService()

print("\nRunning Containers\n")

for c in service.list_running_containers():

    print(c)

print("\nImages\n")

for image in service.list_images():

    print(image)