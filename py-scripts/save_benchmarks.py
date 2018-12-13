# Author: Ammar Hasan 150454388 November 2018
# Purpose: saves benchmarks to db

import pymongo
import requests
import json

# Hosts
MONGO_HOST = "mongodb://127.0.0.1:3306/"
ADVISOR_HOST = "http://localhost:3000/api/v1.3/"

# get mongo client
my_client = pymongo.MongoClient(MONGO_HOST)

my_db = my_client["benchdb"]
my_col = my_db["benchcollection"]

res = requests.get(ADVISOR_HOST + "subcontainers/docker/")
js_arr = res.json()

for container in js_arr:
    #print(container.keys())
    if "id" in container.keys():
        id = container['id']
        name = container['labels']['com.docker.swarm.service.name']
        json_stats = container['stats']
        my_dict = { "id": id, "name": name, "jsonStats" : json_stats }
        x = my_col.insert_one(my_dict)
