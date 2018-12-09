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

# Record starting time stamp
start_time = datetime.datetime.now()

# save to db

# Hosts
MONGO_HOST = "mongodb://127.0.0.1:3306/"
ADVISOR_HOST = "http://localhost:3000/api/v1.3/"

# get mongo client
my_client = pymongo.MongoClient(MONGO_HOST)

# find db and collection
my_db = my_client["benchdb"]
my_col = my_db["benchcollection"]

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
            stamp = time.strptime(stat['timestamp'][:-4], '%Y-%m-%dT%H:%M:%S.%f')
            print(stamp)
