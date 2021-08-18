from locale import atoi
import pymongo
import Config
import urllib
from math import sqrt
import numpy as np
import json
from bson.json_util import dumps
from bson.json_util import loads
import json
from json import encoder
from bson import ObjectId, json_util


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


#########################################################################################################################
class DataBase:
    def __init__(self):
        client = pymongo.MongoClient(
            # f"mongodb+srv://{Config.DB_USER}:{urllib.parse.quote(Config.DB_PASS)}@cluster0.ibr9d.mongodb.net/{Config.DB_NAME}?retryWrites=true&w=majority"
            "mongodb+srv://ARKhaled:Bodyflash149@cluster0.ahlri.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE'
        )
        self.db = client.All
        print("connected to the DB!")
########################################################################################################################
    def insertbike(self, params):
        db = self.db.bike
        cursor = list(db.find())
        for record in cursor:
            if record["Name"] == params["Name"]:
                return None
        return loads(dumps(db.insert(params)))
#########################################################################################################################
    def getbike(self, params=None):
        db = self.db.bike
        cursor = list(db.find())
        for record in cursor:
            if record["Name"] == params["Name"]:
                return loads(dumps(record))
        return None
#########################################################################################################################
    def getallbike(self):
        db = self.db.bike
        cursor = list(db.find())
        if cursor is None:
            return loads(dumps(cursor))
        else:
            return cursor
#########################################################################################################################
    def get_locations(self, params):
        db = self.db.bike
        min_distance = 999999
        min_infra = None
        min_number = atoi(params["Number"])
        East = float(params["East"])
        North = float(params["North"])
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
    def UpdateBike(self, params):
        db = self.db.bike
        cursor = list(db.find())
        for record in cursor:
            if record["Name"] == params["Name"]:
                values = {"$set": {"East": params["East"],
                                   "North": params["North"],
                                   "Locked": params["Locked"],
                                   "Shared": params["Shared"],
                                   "Speed": params["Speed"],
                                   "IP": params["IP"],
                                   "Port": params["Port"],
                                   "Execute":params["Execute"],
                                   "Command": params["Command"],
                                   "Current_Network_Name":params['Current_Network_Name'],
                                   "Current_Network_Password": params['Current_Network_Password']
                                   }}
                return loads(dumps(str(db.update_one(record, values))))
        return None
#########################################################################################################################


    def updateCommand(self,params):
        cursor1= self.db.bike.find()            
        for record in cursor1:
            
            if record['Name'] == params['Name']:
               
              self.db.bike.find_one_and_update({"Name" : params['Name']},{"$set":{"Command": params["Command"], "Execute":"True"}},upsert=True)
              return {"error": False, "message":"Done!"}  
            
                             
        return {"error": True, "message": "Bike not found"}
#########################################################################################################################
    def lockBike(self,params):
        cursor1= self.db.bike.find()            
        for record in cursor1:
            
            if record['Name'] == params['Name']:
               
              self.db.bike.find_one_and_update({"Name" : params['Name']},{"$set":{"Locked":"True"}},upsert=True)
              return {"error": False, "message":"Done!"}  
            
                             
        return {"error": True, "message": "Bike not found"}
    
#########################################################################################################################

    def unlockBike(self,params):
        cursor1= self.db.bike.find()            
        for record in cursor1:
            
            if record['Name'] == params['Name']:
               
              self.db.bike.find_one_and_update({"Name" : params['Name']},{"$set":{"Locked":"False"}},upsert=True)
              return {"error": False, "message":"Done!"}  
            
                             
        return {"error": True, "message": "Bike not found"}
    
#########################################################################################################################

    def updateBike2(self,params):
        cursor1= self.db.bike.find()            
        for record in cursor1:
            
            if record['Name'] == params['Name']:
               
              self.db.bike.find_one_and_update({"Name" : params['Name']},{"$set":{"East": params["East"], "North":params["East"],"Speed": params["Speed"] }},upsert=True)
              return {"error": False, "message":"Done!"}  
            
                             
        return {"error": True, "message": "Bike not found"}
