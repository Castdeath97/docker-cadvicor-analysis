# Author: Ammar Hasan 150454388 November 2018
# Purpose: start swarm of benchmark (2), mongo and visualiser

import docker

# Images
PRIME_IMAGE = "nclcloudcomputing/javabenchmarkapp"
VISUAL_IMAGE = "dockersamples/visualizer"
MONGO_IMAGE = "mongo"

# Replicas for prime web
PRIME_REP = 2

# docker client
client = docker.from_env() 
 # start swarm
client.swarm.init()
# create network
net = client.networks.create(name = "webnet", scope = "swarm", driver = "overlay") 

# Services (all in the same swarm network (networks = [net.id]))

# prime webserver (port 8080<>8080)
client.services.create(
    name = "prime",
    image = PRIME_IMAGE, 
    networks = [net.id],
    endpoint_spec = docker.types.EndpointSpec(ports = {8080:8080})
    ).scale(PRIME_REP) # scale for replicas

# docker visualiser webserver (port 3000<>8080)
# set up required vols and constraints specfied in its github
client.services.create(
    name = "visualizer",
    image = VISUAL_IMAGE, networks = [net.id], 
    constraints = ["node.role == manager"],
    mounts = [ "/:/rootfs:ro","/var/run:/var/run:ro","/sys:/sys:ro"
    ,"/var/lib/docker/:/var/lib/docker:ro","/dev/disk/:/dev/disk:ro"],
    endpoint_spec = docker.types.EndpointSpec(ports = {4000:8080})
    )

# mongo database (port 3306<>27017)
# set up vol for presistence 
client.services.create(
    name = "mongo",
    image = MONGO_IMAGE,
    networks = [net.id],
    mounts = ["/data/db"],
    endpoint_spec = docker.types.EndpointSpec(ports = {3306:27017})
    )