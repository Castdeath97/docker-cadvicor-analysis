#!/usr/bin/env python

# Author: Ammar Hasan 150454388 December 2018
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
import re

#MONGO_HOST = "mongodb://127.0.0.1:3306/"
#ADVISOR_HOST = "http://localhost:3000/api/v1.3/"

MONGO_HOST = "mongodb://35.197.228.218:3306/"
ADVISOR_HOST = "http://35.197.228.218:3000/api/v1.3/"
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
BENCH_DURATION = 60

# Setup required arguments
parser = argparse.ArgumentParser("distr")
parser.add_argument("method", help="normal(0) or poi(1) for poission", type=int)
parser.add_argument("url", help="URL to send requests to", type=str)
parser.add_argument("mean", help="Mean/Lambda intreval time for requests (ms)", type=float)
parser.add_argument("sigma", help="Standard Deviation for time (ms)", type=float)
args = parser.parse_args() # get arguments

# return time to sleep/wait based on method
def get_sleep_time():
    if(args.method == 1):
        return(1 / abs(numpy.random.exponential(args.mean)))
    else:
        return(abs(numpy.random.normal(args.mean, args.sigma, 1)[0]))

# Record starting time stamp
start_time = time.time()

# Prime times list
prime_times = []

# program loop for runtime
while ((time.time() - start_time) < BENCH_DURATION) : 
    # get time to sleep using method 
    sleep_time = get_sleep_time()
    time.sleep(sleep_time/1000)

    # make request after sleep and report
    r = requests.get(args.url) 
    print("request made after: " + str(round(sleep_time,4)) 
    + "ms server says: \"" + r.text + "\"")
    print((time.time() - start_time))
    prime_times.append(r.text) # record prime time calculation

# extract integers from prime calculation
for i in range(len(prime_times)):
    prime_times[i] =  int(re.search(r'\d+', prime_times[i]).group())
print(prime_times)
# record benchmark finish time
finish_time =  time.time()

# save to db

# get mongo client
my_client = pymongo.MongoClient(MONGO_HOST)

# find db and collection
my_db = my_client["benchdb"]

# remove if stat collection exists to make a new one 
if("statcollection" in my_db.list_collection_names()):
    my_db["statcollection"].drop()   
stat_col = my_db["statcollection"]

# remove if prime calculation collection exists to make a new one
if("primecollection" in my_db.list_collection_names()):
    my_db["primecollection"].drop()   
prime_calc_col = my_db["primecollection"]

# record prime calculation 
prime_calc_col.insert_one({"time": prime_times})

# get json trees
res = requests.get(ADVISOR_HOST + "subcontainers/docker/")
js_arr = res.json()

# iterate json trees
for container in js_arr:
    if "id" in container.keys():
        docker_id = container['id']
        name = container['labels']['com.docker.swarm.service.name']
        json_stats = container['stats']

        stat_list = []
        # iterate stats json tree, insert if between start and finish
        for stat in json_stats:
            stat_time = datetime.datetime.strptime(stat['timestamp'][:-4], DATE_TIME_FORMAT).timestamp()
            if stat_time > start_time and stat_time < finish_time:
                stat_list.append(stat)

        # convert python list to a json to store
        # Make an entry when done
        my_dict = { "id":  docker_id, "name": name, "stats": stat_list }
        stat_col.insert_one(my_dict)
