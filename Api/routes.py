import flask
from flask_caching import Cache
import requests
import json
from flask import Flask, jsonify, request, Response
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "key"
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
auth = "main"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            txt = {"Action": 'Token is missing', "date": datetime.datetime.utcnow()}
            # jsontxt = json.dumps(txt)
            jsonFile = open("log.json", 'w')
            # jsonFile.write(jsontxt)
            jsonFile.close()

            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
            print(data)
        except:
            txt = {"Action": 'Token is Invalid', "date": datetime.datetime.utcnow()}
            # jsontxt = json.dumps(txt)
            jsonFile = open("log.json", 'w')
            # jsonFile.write(jsontxt)
            jsonFile.close()
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def Welcome():
    return "Welcome to the Main Server!"


# Bike Routes
@app.route('/bikes/Addbike', methods=['POST'])
def AddBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/Addbike", data={'Token': token,
                                                                                    "East": request.form['East'],
                                                                                    "North": request.form['North'],
                                                                                    "Name": request.form['Name'],
                                                                                    "Locked": request.form['Locked'],
                                                                                    "Speed": request.form['Speed'],
                                                                                    "Shared": request.form['Shared'],
                                                                                    "IP": request.form['IP'],
                                                                                    "Port": request.form['Port'],
                                                                                    "Execute": request.form['Execute'],
                                                                                    "Command": request.form['Command'],
                                                                                    "Current_Network_Name":
                                                                                        request.form[
                                                                                            'Current_Network_Name'],
                                                                                    "Current_Network_Password":
                                                                                        request.form[
                                                                                            'Current_Network_Password']
                                                                                    })
    return "Bike Server Communicated!"


@app.route('/bikes/getbike', methods=['POST'])
def getBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/getbike", data={'Token': token,
                                                                                    'Name': request.form["Name"]})
    return "Bike Server Communicated!"


@app.route('/bikes', methods=['POST'])
def getAllBikes():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes", data={'Token': token})
    return "Bike Server Communicated!"


@app.route('/bikes/NearestBikes', methods=['POST'])
def get_location():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/NearestBikes", data={'Token': token,
                                                                                         "East": request.form["East"],
                                                                                         "North": request.form["North"],
                                                                                         "Number": request.form[
                                                                                             "Number"]})
    return "Bike Server Communicated!"


@app.route('/bikes/UpdateBike', methods=['POST'])
def UpdateBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/UpdateBike", data={'Token': token,
                                                                                       "East": request.form["East"],
                                                                                       "North": request.form["North"],
                                                                                       "Name": request.form["Name"],
                                                                                       "Locked": request.form["Locked"],
                                                                                       "Speed": request.form["Speed"],
                                                                                       "Shared": request.form["Shared"],
                                                                                       "IP": request.form["IP"],
                                                                                       "Port": request.form["Port"],
                                                                                       "Execute": request.form[
                                                                                           "Execute"],
                                                                                       "Command": request.form[
                                                                                           "Command"],
                                                                                       "Current_Network_Name":
                                                                                           request.form[
                                                                                               'Current_Network_Name'],
                                                                                       "Current_Network_Password":
                                                                                           request.form[
                                                                                               'Current_Network_Password']})
    return "Bike Server Communicated!"


@app.route('/bikes/updateCommand', methods=['POST'])
def updateCommand():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/updateCommand", data={'Token': token,
                                                                                          "Name": request.form["Name"],
                                                                                          "Command": request.form[
                                                                                              "Command"]})
    return "Bike Server Communicated!"


@app.route('/bikes/lockBike', methods=['POST'])
def updateLocked():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/lockBike", data={'Token': token,
                                                                                     "Name": request.form["Name"]})
    return "Bike Server Communicated!"


@app.route('/bikes/unlockBike', methods=['POST'])
def updateunLocked():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/unlockBike", data={'Token': token,
                                                                                       "Name": request.form["Name"]})
    return "Bike Server Communicated!"


@app.route('/bikes/updateBike2', methods=['POST'])
def updateBike2():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/updateBike2", data={'Token': token,
                                                                                        "Name": request.form["Name"],
                                                                                        "North": request.form["North"],
                                                                                        "East": request.form["East"],
                                                                                        "Speed": request.form["Speed"]
                                                                                        })
    return "Bike Server Communicated!"


@app.route('/bikes/shareBike', methods=['POST'])
def sharebike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/shareBike", data={'Token': token,
                                                                                      "Name": request.form["Name"],
                                                                                      "North": request.form["North"],
                                                                                      "East": request.form["East"],
                                                                                      "Speed": request.form["Speed"]
                                                                                      })
    return "Bike Server Communicated!"


@app.route('/bikes/stopShareBike', methods=['POST'])
def stopsharebike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/stopShareBike", data={'Token': token,
                                                                                          "Name": request.form["Name"],
                                                                                          "North": request.form[
                                                                                              "North"],
                                                                                          "East": request.form["East"],
                                                                                          "Speed": request.form[
                                                                                              "Speed"]})
    return "Bike Server Communicated!"


@app.route('/bikes/editPrice', methods=['POST'])
def editPrice():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/editPrice", data={'Token': token,
                                                                                      "Name": request.form["Name"],
                                                                                      "North": request.form["North"],
                                                                                      "East": request.form["East"],
                                                                                      "Speed": request.form["Speed"]
                                                                                      })
    return "Bike Server Communicated!"


@app.route('/bikes/getbikePrice/<name>', methods=['POST'])
def getBikePrice(name):
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/getbikePrice/<name>", data={'Token': token,
                                                                                                "Name": request.form["Name"],
                                                                                                "North": request.form["North"],
                                                                                                "East": request.form["East"],
                                                                                                "Speed": request.form["Speed"]
                                                                                                })
    return "Bike Server Communicated!"


@app.route('/bikes/getBikeLocked/<name>', methods=['POST'])
def getBikeLocked(name):
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/getBikeLocked/<name>", data={'Token': token,
                                                                                                "Name": request.form["Name"],
                                                                                                "North": request.form["North"],
                                                                                                "East": request.form["East"],
                                                                                                "Speed": request.form["Speed"]
                                                                                                })
    return "Bike Server Communicated!"


@app.route('/bikes/getBikeShared/<name>', methods=['POST'])
def getBikeShared(name):
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-bike.herokuapp.com/bikes/getBikeShared/<name>", data={'Token': token,
                                                                                                "Name": request.form["Name"],
                                                                                                "North": request.form["North"],
                                                                                                "East": request.form["East"],
                                                                                                "Speed": request.form["Speed"]
                                                                                                })
    return "Bike Server Communicated!"


# User Routes
@app.route('/users/sendemail', methods=['POST'])
def sendEmail():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/sendemail", data={'Token': token})
    return "User Server Communicated!"


@app.route('/users/register', methods=['POST'])
def createUser():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/register", data={'Token': token,
                                                                                "fname": request.form["fname"],
                                                                                "lname": request.form["lname"],
                                                                                "email": request.form["email"],
                                                                                "password": request.form["password"]
                                                                                })
    return "User Server Communicated!"


@app.route('/users/getuserbike/<email>', methods=['POST'])
def getUserbike(email):
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/getuserbike/<email>", data={'Token': token})
    return "User Server Communicated!"


@app.route('/users/getusertempbike/<email>', methods=['POST'])
def getUserTempBike(email):
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/getusertempbike/<email>", data={'Token': token})
    return "User Server Communicated!"


@app.route('/users/getcommand', methods=['POST'])
def getCMD():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/getcommand", data={'Token': token,
                                                                                  "email": request.form['email']})
    return "User Server Communicated!"


@app.route('/users/updatebikeid', methods=['POST'])
def updateBikeID():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/updatebikeid", data={'Token': token,
                                                                                    "email": request.form['email']})
    return "User Server Communicated!"


@app.route('/users/updatetempbikeid', methods=['POST'])
def updateTempBikeID():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/updatetempbikeid", data={'Token': token,
                                                                                        "email": request.form['email']})
    return "User Server Communicated!"


@app.route('/users/nullifybikeid', methods=['POST'])
def nullifyBikeID():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/nullifybikeid", data={'Token': token,
                                                                                     "email": request.form['email']})
    return "User Server Communicated!"


@app.route('/users/addnumber', methods=['POST'])
def addNumber():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/addnumber", data={'Token': token,
                                                                                 "email": request.form['email'],
                                                                                 "numbers": request.form['numbers']})
    return "User Server Communicated!"


@app.route('/users/editnumber', methods=['POST'])
def editNumber():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/editnumber", data={'Token': token,
                                                                                  "email": request.form['email'],
                                                                                  "numbers": request.form['numbers']})
    return "User Server Communicated!"


@app.route('/users/removenumber', methods=['POST'])
def removeNumber():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/removenumber", data={'Token': token,
                                                                                    "email": request.form['email'],
                                                                                    "numbers": request.form['numbers']})
    return "User Server Communicated!"


@app.route('/users/gimmenums/<email>', methods=['POST'])
def getEmergencyNumbers(email):
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/gimmenums/<email>", data={'Token': token})
    return "User Server Communicated!"


@app.route('/users/createRide', methods=['POST'])
def createRide():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/createRide", data={'Token': token,
                                                                                  "email": request.form["email"],
                                                                                  "rideNo": request.form["rideNo"],
                                                                                  "history": request.form["history"],
                                                                                  "startDate": request.form[
                                                                                      "startDate"],
                                                                                  "endDate": request.form["endDate"],
                                                                                  "startTime": request.form[
                                                                                      "startTime"],
                                                                                  "endTime": request.form["endTime"]})
    return "User Server Communicated!"


@app.route('/users/removeride', methods=['POST'])
def removeRide():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/removeride", data={'Token': token,
                                                                                  "email": request.form["email"],
                                                                                  "rideNo": request.form["rideNo"]})
    return "User Server Communicated!"


@app.route('/users/getrides/<email>', methods=['POST'])
def getRides(email):
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/getrides/<email>", data={'Token': token})
    return "User Server Communicated!"


@app.route('/users/checkemail', methods=['POST'])
def checkEmail():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/checkemail", data={'Token': token,
                                                                                  "email": request.form["email"]})
    return "User Server Communicated!"


@app.route('/users/emailVal', methods=['POST'])
def emailVall():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/emailVal", data={'Token': token,
                                                                                "email": request.form["email"]})
    return "User Server Communicated!"


@app.route('/users/forgotpassword', methods=['POST'])
def forgotPW():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/forgotpassword", data={'Token': token,
                                                                                      "email": request.form["email"]})
    return "User Server Communicated!"


@app.route('/users/checkcode', methods=['POST'])
def checkcode():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/checkcode", data={'Token': token,
                                                                                 "email": request.form["email"],
                                                                                 "code": request.form["code"]})
    return "User Server Communicated!"


@app.route('/users/changepwez', methods=['POST'])
def changePWEZ():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/changepwez", data={'Token': token,
                                                                                  "email": request.form["email"],
                                                                                  "newpw": request.form["newpw"]})
    return "User Server Communicated!"


@app.route('/users/removecode', methods=['POST'])
def removecode():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/removecode", data={'Token': token,
                                                                                  "email": request.form["email"],
                                                                                  "code": request.form["code"]})
    return "User Server Communicated!"


@app.route('/users/login', methods=['POST'])
def login():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/login", data={'Token': token,
                                                                             "email": request.form["email"],
                                                                             "password": request.form["password"]})
    return "User Server Communicated!"


@app.route('/users/changepw', methods=['POST'])
def changepw():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-users.herokuapp.com/users/changepw", data={'Token': token,
                                                                                "email": request.form["email"],
                                                                                "password": request.form["password"]})
    return "User Server Communicated!"


# Car Routes
@app.route('/cars/addcar', methods=['POST'])
def AddCar():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/cars/addcar", data={'Token': token,
                                                                                 "North": request.form['North'],
                                                                                 "East": request.form['East'],
                                                                                 "Name": request.form['Name'],
                                                                                 "IP": request.form['IP'],
                                                                                 "Port": request.form['Port'],
                                                                                 "Key": request.form["Key"]})
    return "Car Server Communicated!"


@app.route('/cars/getcar', methods=['POST'])
def getCar():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/cars/getcar", data={'Token': token,
                                                                                 "Name": request.form['Name']})
    return "Car Server Communicated!"


@app.route('/cars', methods=['POST'])
def getAllCars():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/cars", data={'Token': token})
    return "Car Server Communicated!"


@app.route('/cars/Nearestcar', methods=['POST'])
def getlocationcars():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/cars/Nearestcar", data={'Token': token,
                                                                                     "East": request.form["East"],
                                                                                     "North": request.form["North"],
                                                                                     "Number": request.form["Number"]})
    return "Car Server Communicated!"


@app.route('/cars/UpdateCar', methods=['POST'])
def Updatecar():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/cars/UpdateCar", data={'Token': token,
                                                                                    "Name": request.form['Name'],
                                                                                    "Key": request.form["Key"]})
    return "Car Server Communicated!"


# Infra Routes
@app.route('/infrastructures/addbasestation', methods=['POST'])
def AddInfra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/infrastructures/addbasestation", data={'Token': token,
                                                                                         "Name": request.form['Name'],
                                                                                         "North": request.form['North'],
                                                                                         "East": request.form['East'],
                                                                                         "IP": request.form['IP'],
                                                                                         "Public_Key": request.form[
                                                                                             'Public_Key'],
                                                                                         "Password": request.form[
                                                                                             "Password"]})
    return "Infra Server Communicated!"


@app.route('/infrastructures/getbasestation', methods=['POST'])
def getInfra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/infrastructures/getbasestation", data={'Token': token,
                                                                                         "Name": request.form["Name"]})
    return "Infra Server Communicated!"


@app.route('/infrastructures', methods=['POST'])
def getAllInfra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/infrastructures", data={'Token': token})
    return "Infra Server Communicated!"


@app.route('/infrastructures/Nearestbs', methods=['POST'])
def get_location_infra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    r = requests.post(url="https://sdb-app-carinfra.herokuapp.com/infrastructures/Nearestbs", data={'Token': token,
                                                                                    "East": request.form["East"],
                                                                                    "North": request.form["North"],
                                                                                    "Number": request.form["Number"]})
    return "Infra Server Communicated!"


@app.route('/test/<string>', methods=['GET'])
# @cache.cached(timeout=120)
def test(string):
    print("test")
    # print(f"/test/{string}", flask.request.form)
    helper(string, flask.request.form)
    s = f"test_{flask.request.form['k1']}"
    return s


@cache.memoize(120)
def helper(string, form):
    print("helper", string, form)
    return ""
