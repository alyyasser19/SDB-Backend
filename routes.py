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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/Addbike")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/getbike")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/NearestBikes")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/UpdateBike")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/updateCommand")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/lockBike")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/unlockBike")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/updateBike2")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/sendemail")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/register")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getuserbike/<email>")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getusertempbike/<email>")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getcommand")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/updatebikeid")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/updatetempbikeid")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/nullifybikeid")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/addnumber")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/editnumber")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/removenumber")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/gimmenums/<email>")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/createRide")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/removeride")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/getrides/<email>")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/checkemail")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/emailVal")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/forgotpassword")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/checkcode")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/changepwez")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/removecode")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/login")
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
    try:
        state = flask.request.form["state"]
    except:
        state = 'sent'

    if state == 'sent':
        r = requests.post(url="http://localhost:5001/users/changepw")
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
