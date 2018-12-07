# Author: Ammar Hasan 150454388 Decmber 2018
# Purpose: reads benchmarks back from db

import pymongo
import requests
import json

# Hosts
MONGO_HOST = "mongodb://127.0.0.1:3306/"
ADVISOR_HOST = "http://localhost:3000/api/v1.3/"

# get mongo client
my_client = pymongo.MongoClient(MONGO_HOST)

# setup database and collection
my_db = my_client["benchdb"]
my_col = my_db["benchcollection"]

x = my_col.find_one()
print(x)
