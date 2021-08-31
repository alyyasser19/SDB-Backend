import pymongo
import Config
import urllib 
class DataBase:
    def __init__(self):
        client = pymongo.MongoClient(f"mongodb+srv://{Config.DB_USER}:{urllib.parse.quote(Config.DB_PASS)}@cluster0.ibr9d.mongodb.net/{Config.DB_NAME}?retryWrites=true&w=majority")
        self.db = client.users
        print("connected to the DB!")
