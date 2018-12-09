#!/usr/bin/env python

# Author: Ammar Hasan 150454388 November 2018
# Purpose: Make requests to a URL using poisson process

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
parser = argparse.ArgumentParser("poi")
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("lam", 
help="Lambda for Intreval time of requests (ms)", type=float)
parser.add_argument("runtime", help="running time (seconds)", type=float)
args = parser.parse_args() # get arguments

# Record starting time stamp
start_time = datetime.datetime.now()

# program loop
while ((datetime.datetime.now().second - start_time.second) < args.runtime ) : 
    # get time using numpy exponential (poi process) and sleep with it
    sleep_time = abs(numpy.random.exponential(args.lam)) 
    time.sleep(sleep_time/1000)

    # make request after sleep and report
    r = requests.get(args.url) 
    print("request made after: " + str(round(sleep_time,4)) 
    + "ms server says: \"" + r.text + "\"")

finish_time =  datetime.datetime.now()

# save to db

# Hosts
MONGO_HOST = "mongodb://127.0.0.1:3306/"
ADVISOR_HOST = "http://localhost:3000/api/v1.3/"
FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

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
        # iterate stats json tree
        for stat in json_stats:
            stat_time = datetime.datetime.strptime(stat['timestamp'][:-4], FORMAT)
            if stat_time >= start_time and stat_time <= finish_time:
                my_dict = { "id": id, "name": name, "jsonStats" : stat }
                my_col.insert_one(my_dict)