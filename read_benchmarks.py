import pymongo
import requests
import json

# Hosts
MONGO_HOST = "mongodb://127.0.0.1:3306/"
ADVISOR_HOST = "http://localhost:3000/api/v1.3/"

# get mongo client
myclient = pymongo.MongoClient(MONGO_HOST)

mydb = myclient["benchdb"]
mycol = mydb["benchcollection"]

x = mycol.find_one()
print(x)
