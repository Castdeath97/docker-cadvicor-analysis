# Author: Ammar Hasan 150454388 November 2018
# Purpose: pull and run "nclcloudcomputing/javabenchmarkapp" 

import docker

# Image names
IMAGE_NAME = "nclcloudcomputing/javabenchmarkapp"
CONT_NAME = "prime"
client = docker.from_env() # docker client

# pull image
image = client.images.pull(IMAGE_NAME)

# run container as a daemon with name, print id
container = client.containers.run(IMAGE_NAME, 
    detach=True, name = CONT_NAME, ports = {'8080/tcp': 8080})
