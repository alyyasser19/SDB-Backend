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
    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/Addbike")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/getbike', methods=['POST'])
def getBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/getbike")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes', methods=['POST'])
def getAllBikes():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token

    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/NearestBikes', methods=['POST'])
def get_location():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token

    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/NearestBikes")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/UpdateBike', methods=['POST'])
def UpdateBike():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/UpdateBike")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/updateCommand', methods=['POST'])
def updateCommand():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/updateCommand")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/lockBike', methods=['POST'])
def updateLocked():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/lockBike")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/unlockBike', methods=['POST'])
def updateunLocked():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/unlockBike")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


@app.route('/bikes/updateBike2', methods=['POST'])
def updateBike2():
    token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], "HS256")
    req = flask.make_response(token)
    req.headers['Main_Auth'] = token
    if flask.request.form["state"] == 'sent':
        r = requests.post(url="http://localhost:5001/bikes/updateBike2")
        return req
    if flask.request.form["state"] == 'received':
        print(json.dumps(flask.request.form['Response']))  # testing
        return json.dumps(flask.request.form['Response'])


# User Routes


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
