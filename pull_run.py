# Author: Ammar Hasan 150454388 November 2018
# Purpose pull and load "nclcloudcomputing/javabenchmarkapp" 

import docker

IMAGE_NAME = "nclcloudcomputing/javabenchmarkapp"
CONT_NAME = "benchmarkapp"
client = docker.from_env() # docker client

# pull image, print id
image = client.images.pull(IMAGE_NAME)
#print(image.id)

# run container as a daemon with name, print id
container = client.containers.run(IMAGE_NAME, 
    detach=True, name = CONT_NAME, ports = {'8080/tcp': 8080})
#print(container.id)