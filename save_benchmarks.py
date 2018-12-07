import pymongo
import requests
import json

# Hosts
MONGO_HOST = "mongodb://127.0.0.1:3306/"
ADVISOR_HOST = "http://localhost:3000/api/v1.3/"

# get mongo client
myclient = pymongo.MongoClient(MONGO_HOST)

'''
# check database and create a new one and check
print(myclient.list_database_names())
mydb = myclient["testdb"]
print(myclient.list_database_names())

# add a collection to the database and list the connections
mycol = mydb["testc ollection"]
print(mydb.list_collection_names())

# Insert a record to collection 
mydict = { "name": "John", "address": "Highway 37" }
x = mycol.insert_one(mydict)
print(x.inserted_id)

mydb = myclient["testdb"]
mycol = mydb["testcollection"]

x = mycol.find_one()
print(x)

'''

mydb = myclient["benchdb"]
mycol = mydb["benchcollection"]

res = requests.get(ADVISOR_HOST + "subcontainers/docker/")
jsArr = res.json()

for container in jsArr:
    #print(container.keys())
    if "id" in container.keys():
        id = container['id']
        name = container['labels']['com.docker.swarm.service.name']
        jsonStats = container['stats']
        mydict = { "id": id, "name": name, "jsonStats" : jsonStats }
        x = mycol.insert_one(mydict)

#res = requests.get(ADVISOR_HOST + "subcontainers/docker/")
#js = res.json()[0]

#print(js.keys())
#print(js['labels']['com.docker.swarm.service.name'])
#print(json.dumps(js['labels'], indent=4, sort_keys=True))

#jsSub = js['id']
# print(jsSub.keys())
#print(json.dumps(jsSub, indent=4, sort_keys=True))

#res = requests.get(ADVISOR_HOST + "subcontainers/docker/" + jsSub)
#js = res.json()[0]
#print(js.keys())
#print(json.dumps(js['stats'], indent=4, sort_keys=True))


# http://localhost:8888/api/v1.3/subcontainers/docker