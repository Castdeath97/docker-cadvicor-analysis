# docker-cadvicor-analysis
This repository contains a series of programs used to test and experiement with docker locally and on the cloud (Google Cloud) with the help of cAdvisor.

## File Hierarchy 

*	docker-compose.yml: docker compose file used to deploy stack 
*	sh-scripts: directory used to store shell scripts
       - pull_run.sh: used to pull and run the docker prime check docker image using Linux command line
       - start_swarm.sh: Used to setup swarm stack using Linux shell
       - remove-swarm.sh: Used to remove the stack and swarm when it is initiated with start-swarm using Linux shell 
*	py-scripts: directory used to store python scripts
       - pull_run.py: used to pull and run the docker prime check docker image using Docker’s Python SDK
       - start_swarm.py: Used to setup swarm stack using Docker’s Python SDK
       - distr.py: used to carry analytical load on the server using poisson /normal distribution and stores the results to the mongo database
       - Plots.ipyn: ipython notebook file used to plot the benchmarks stored in the mongo database
*      report.pdf: analysis report
