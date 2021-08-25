import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import requests
from flask_caching import Cache
from Models import Bike, Base_Station
from flask_pymongo import PyMongo

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
app.config["MONGO_URI"] = "dblink"
mongo = PyMongo(app)
cache = Cache(app)

east = Bike.bike["East"]  # mongo.db.bike.find({"East": True})
north = Bike.bike["North"]
speed = Bike.bike["Speed"]
bike_name = Bike.bike["Name"]
locked = Bike.bike["Locked"]
shared = Bike.bike["Shared"]
ip = Bike.bike["IP"]
port = Bike.bike["Port"]
execute = Bike.bike["Execute"]
command = Bike.bike["Command"]
net_name = Bike.bike["Current_Network_Name"]
net_password = Bike.bike["Current_Network_Password"]
station_east = Base_Station.base_station["East"]
station_north = Base_Station.base_station["North"]
station_name = Base_Station.base_station["Name"]
station_pass = Base_Station.base_station["Password"]

bike = {"bikeEast": east, "bikeNorth": north, "Speed": speed, "bikeName": bike_name, "Locked": locked,
        "Shared": shared, "IP": ip, "Port": port, "Execute": execute, "Command": command,
        "Current Network Name": net_name, "Current Network Password": net_password}

base_station = {"stationEast": station_east, "stationNorth": station_north, "stationName": station_name,
                "stationPassword": station_pass}


@app.route('/', methods=['GET'])
def wakeup():
    url = 'https://github.com/alyyasser19/SDB-Backend/blob/main/auth.py'  # change with deployed heroku server
    requests.get(url)
    requests.post(url, data="")
    url1 = 'https://github.com/alyyasser19/SDB-Backend/blob/bike/auth.py'
    requests.get(url1)
    requests.post(url1, data="")
    requests.get(url)
    requests.post(url, data="")
    url2 = 'https://github.com/alyyasser19/SDB-Backend/blob/carinfra/auth.py'
    requests.get(url2)
    requests.post(url2, data="")
    requests.get(url)
    requests.post(url, data="")
    url3 = 'https://github.com/alyyasser19/SDB-Backend/blob/users/auth.py'
    requests.get(url3)
    requests.post(url3, data="")
    requests.get(url)
    requests.post(url, data="")


scheduler = BackgroundScheduler()
scheduler.add_job(func=wakeup, trigger="interval", minutes=30)
scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True)
