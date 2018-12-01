# Author: Ammar Hasan 150454388 November 2018
# Purpose: start swarm of benchmark (2), mongo and visualiser

import docker

client = docker.from_env() # docker client
client.swarm.init() # start swarm
client.services.create

#docker stack deploy -c docker-compose.yml benchmarkswarm

