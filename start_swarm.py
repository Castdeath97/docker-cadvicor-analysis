# Author: Ammar Hasan 150454388 November 2018
# Purpose: start swarm of benchmark (2), mongo and visualiser

import docker

# Images
PRIME_IMAGE = "nclcloudcomputing/javabenchmarkapp"
VISUAL_IMAGE = "dockersamples/visualizer"
MONGO_IMAGE = "mongo"

# Replicas
BENCH_REP = 2

client = docker.from_env() # docker client
client.swarm.init() # start swarm
net = client.networks.create("network", scope = "swarm") # create network

# Services

client.services.create(image = PRIME_IMAGE, networks = net.id).scale(BENCH_REP)
client.services.create(image = VISUAL_IMAGE, networks = net.id, constraints = "node.role == manager")
client.services.create(image = MONGO_IMAGE, networks = net.id)

# vol, , port