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
    return "Welcome to the app!"


# Bike Routes
@app.route('/bikes/Addbike', methods=['POST'])
def AddBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/Addbike", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/getbike', methods=['POST'])
def getBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/getbike", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes', methods=['POST'])
def getAllBikes():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])



@app.route('/bikes/NearestBikes', methods=['POST'])
def get_location():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/NearestBikes", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/UpdateBike', methods=['POST'])
def UpdateBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/UpdateBike", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/updateCommand', methods=['POST'])
def updateCommand():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/updateCommand", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/lockBike', methods=['POST'])
def updateLocked():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/lockBike", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/unlockBike', methods=['POST'])
def updateunLocked():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/unlockBike", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/updateBike2', methods=['POST'])
def updateBike2():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/updateBike2", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])

# User Routes
@app.route('/users/sendemail', methods=['POST'])
def sendEmail():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/sendemail", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/register', methods=['POST'])
def createUser():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/register", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/getuserbike/<email>', methods=['POST'])
def getUserbike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getuserbike/<email>", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/getusertempbike/<email>', methods=['POST'])
def getUserTempBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getusertempbike/<email>", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/getcommand', methods=['POST'])
def getCMD():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getcommand", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/updatebikeid', methods=['POST'])
def updateBikeID():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/updatebikeid", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/updatetempbikeid', methods=['POST'])
def updateTempBikeID():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/updatetempbikeid", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/nullifybikeid', methods=['POST'])
def nullifyBikeID():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/nullifybikeid", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/addnumber', methods=['POST'])
def addNumber():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/addnumber", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/editnumber', methods=['POST'])
def editNumber():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/editnumber", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/removenumber', methods=['POST'])
def removeNumber():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/removenumber", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/gimmenums/<email>', methods=['POST'])
def getEmergencyNumbers():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/gimmenums/<email>", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/createRide', methods=['POST'])
def createRide():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/createRide", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/removeride', methods=['POST'])
def removeRide():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/removeride", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/getrides/<email>', methods=['POST'])
def getRides():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getrides/<email>", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/checkemail', methods=['POST'])
def checkEmail():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/checkemail", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/emailVal', methods=['POST'])
def emailVall():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/emailVal", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/forgotpassword', methods=['POST'])
def forgotPW():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/forgotpassword", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/checkcode', methods=['POST'])
def checkcode():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/checkcode", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/changepwez', methods=['POST'])
def changePWEZ():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/changepwez", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/removecode', methods=['POST'])
def removecode():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/removecode", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/login', methods=['POST'])
def login():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/login", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/users/changepw', methods=['POST'])
def changepw():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/changepw", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])

# Car Routes
@app.route('/cars/addcar', methods=['POST'])
def AddCar():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/cars/addcar", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/cars/getcar', methods=['POST'])
def getCar():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/cars/getcar", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/cars', methods=['POST'])
def getAllCars():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/cars", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/cars/Nearestcar', methods=['POST'])
def getlocationcars():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/cars/Nearestcar", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/cars/UpdateCar', methods=['POST'])
def Updatecar():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/cars/UpdateCar", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])

# Infra Routes
@app.route('/infrastructures/addbasestaion', methods=['POST'])
def AddInfra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/infrastructures/addbasestaion", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/infrastructures/getbasestation', methods=['POST'])
def getInfra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/infrastructures/getbasestation", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/infrastructures', methods=['POST'])
def getAllInfra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/infrastructures", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/infrastructures/Nearestbs', methods=['POST'])
def get_location_infra():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    data = {'Token': token}
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/infrastructures/Nearestbs", data=data)
        return req
    if state == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


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
