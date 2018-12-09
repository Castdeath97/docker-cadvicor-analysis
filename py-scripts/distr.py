#!/usr/bin/env python

# Author: Ammar Hasan 150454388 November 2018
# Purpose: Make requests to a URL using poisson or normal process

import signal
import sys
import argparse
import numpy
import requests
import time
import datetime
import pymongo
import json

# Setup required arguments
parser = argparse.ArgumentParser("distr")
parser.add_argument("method", help="normal(0) or poi(1) for poission", type=int)
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("mean", help="Mean/Lambda intreval time for requests (ms)", type=float)
parser.add_argument("sigma", help="Standard Deviation for time (ms)", type=float)
parser.add_argument("runtime", help="running time (seconds)", type=float)
args = parser.parse_args() # get arguments

# return time to sleep/wait based on method
def get_sleep_time():
    if(args.method == 0):
        return(abs(numpy.random.exponential(args.mean)))
    else:
        return(abs(numpy.random.normal(args.mean, args.sigma, 1)[0]))


# Record starting time stamp
start_time = datetime.datetime.now()

# program loop for runtime
while ((datetime.datetime.now().second - start_time.second) < args.runtime ) : 
    # get time to sleep using method 
    sleep_time = get_sleep_time()
    time.sleep(sleep_time/1000)

    # make request after sleep and report
    r = requests.get(args.url) 
    print("request made after: " + str(round(sleep_time,4)) 
    + "ms server says: \"" + r.text + "\"")

# record benchmark finish time
finish_time =  datetime.datetime.now()

# save to db

# Hosts
MONGO_HOST = "mongodb://127.0.0.1:3306/"
ADVISOR_HOST = "http://localhost:3000/api/v1.3/"

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

# get mongo client
my_client = pymongo.MongoClient(MONGO_HOST)

# find db and collection
my_db = my_client["benchdb"]
my_col = my_db["statcollection"]

# get json trees
res = requests.get(ADVISOR_HOST + "subcontainers/docker/")
js_arr = res.json()

# iterate json trees
for container in js_arr:
    if "id" in container.keys():
        id = container['id']
        name = container['labels']['com.docker.swarm.service.name']
        json_stats = container['stats']

        # iterate stats json tree, insert if between start and finish
        for stat in json_stats:
            stat_time = datetime.datetime.strptime(stat['timestamp'][:-4], DATE_TIME_FORMAT)
            if stat_time >= start_time and stat_time <= finish_time:
                my_dict = { "id": id, "name": name, "jsonStats" : stat }
                my_col.insert_one(my_dict)