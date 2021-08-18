from locale import atoi
import pymongo
import Config
import urllib
from math import sqrt
import numpy as np
from bson.json_util import dumps
from bson.json_util import loads
########################################################################################################################
class DataBase:
    def __init__(self):
        client = pymongo.MongoClient(
            # f"mongodb+srv://{Config.DB_USER}:{urllib.parse.quote(Config.DB_PASS)}@cluster0.ibr9d.mongodb.net/{Config.DB_NAME}?retryWrites=true&w=majority")
            "mongodb+srv://ARKhaled:Bodyflash149@cluster0.ahlri.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        )
        self.db = client.All
        print("connected to the DB!")
########################################################################################################################
    def insertbs(self, database, params):
        if database == "basestation":
            db = self.db.basestation
        elif database == "car":
            db = self.db.car
        else:
            db = None
            return
        cursor = list(db.find())
        for record in cursor:
            if record["Name"] == params["Name"]:
                return None
        return loads(dumps(db.insert(params)))
#########################################################################################################################
    def getbs(self, database, params):
        if database == "basestation":
            db = self.db.basestation
        elif database == "car":
            db = self.db.car
        else:
            db = None
            return
        cursor = list(db.find())
        for record in cursor:
            if record["Name"] == params["Name"]:
                return loads(dumps(record))
        return None
########################################################################################################################
    def getallbs(self,database):
        if database == "basestation":
            db = self.db.basestation
        elif database == "car":
            db = self.db.car
        else:
            db = None
            return
        cursor = list(db.find())
        if cursor is None:
            return loads(dumps(cursor))
        else:
            return cursor
########################################################################################################################
    def get_locations(self, database, params):
        if database == "basestation":
            db = self.db.basestation
        elif database == "car":
            db = self.db.car
        else:
            db = None
            return
        min_distance = 999999
        min_infra = None
        min_number = atoi(params["Number"])
        East = float(params["East"])
        North = float(params["North"])
        # print(type(East), type(North))
        # print(min_number)
        min_array = [None for _ in range(min_number)]
        min_dist = [10_000 for _ in range(min_number)]
        cursor = list(db.find())
        for doc in cursor:
            distance = sqrt(((East - float(doc["East"])) ** 2 + (North - float(doc["North"])) ** 2))
            if distance < max(min_dist):
                index = np.argmax(min_dist)
                min_dist[index] = distance
                min_array[index] = doc
        return loads(dumps(min_array))  
#########################################################################################################################
    def UpdateCar(self, params):
        cursor1= self.db.car.find()            
        for record in cursor1:   
            if record['Name'] == params['Name']: 
                
                self.db.users.find_one_and_update({"Name" : params['Name']},{"$set":{"Key": params["Key"]}},upsert=True)
                
                return {"error": False, "message":"Car Key updated"}                
        return {"error": True, "message": "Car not found"}