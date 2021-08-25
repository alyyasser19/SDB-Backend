import atexit
from enum import Enum
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import requests
from flask_caching import Cache
from Models import Cars, Base_Station

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}


app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

east = Cars.car["East"]
north = Cars.car["North"]
speed = Cars.car["Speed"]
bike_name = Cars.car["Name"]
locked = Cars.car["Locked"]
shared = Cars.car["Shared"]
ip = Cars.car["IP"]
port = Cars.car["Port"]
execute = Cars.car["Execute"]
command = Cars.car["Command"]
net_name = Cars.car["Current_Network_Name"]
net_password = Cars.car["Current_Network_Password"]
station_east = Base_Station.base_station["East"]
station_north = Base_Station.base_station["North"]
station_name = Base_Station.base_station["Name"]
station_pass = Base_Station.base_station["Password"]

bike = {"bikeEast": east, "bikeNorth": north, "Speed": speed, "bikeName": bike_name, "Locked": locked,
        "Shared": shared, "IP": ip, "Port": port, "Execute": execute, "Command": command,
        "Current Network Name": net_name, "Current Network Password": net_password}

base_station = {"stationName": station_name, "stationPassword": station_pass, "stationEast": station_east,
                "stationNorth": station_north}


@app.route('/', methods= ['GET'])
def wakeup():
    url = 'https://github.com/alyyasser19/SDB-Backend/blob/main/auth.py'
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
    return


scheduler = BackgroundScheduler()
scheduler.add_job(func=wakeup, trigger="interval", minutes=30)
scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))


if __name__ == '__main__':
    app.run(debug=True)