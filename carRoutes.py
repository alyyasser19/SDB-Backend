import flask
import jwt
import requests

from routes import app
from flask import request, Response
from DataBase import DataBase
from Cars import validate
import json

db = DataBase()
app.config["SECRET_KEY"] = "key"


########################################################################################################################
@app.route('/cars/addcar', methods=['POST'])
def AddCar():
    token = flask.request.form["Token"]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 403,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/addcar", data=data)
        return resp
    validated = validate(request.form)
    error = validated["error"]
    output = dict()
    if not error:
        info = {"North": request.form['North'],
                "East": request.form['East'],
                "Name": request.form['Name'],
                "IP": request.form['IP'],
                "Port": request.form['Port'],
                "Key": request.form["Key"]}
        x = db.insertbs("car", info)
        output = dict()
        output['data'] = None
        if x is None:
            output['message'] = 'name is not unique'
            output['error'] = True
        else:
            output['message'] = 'Success'
            output['error'] = False
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/addcar", data=data)
        return resp
    else:
        x = None
        output['data'] = x
        output['message'] = validated["message"]
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/addcar", data=data)
        return resp


########################################################################################################################
@app.route('/cars/getcar', methods=['POST'])
def getCar():
    token = flask.request.form["Token"]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 403,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/getcar", data=data)
        return resp
    info = {
        "Name": request.form["Name"]
    }
    x = db.getbs("car", info)
    output = dict()
    if x is not None:
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/getcar", data=data)
        return resp
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/getcar", data=data)
        return resp


########################################################################################################################
@app.route('/cars', methods=['POST'])
def getAllCars():

    token = flask.request.form["Token"]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 403,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars", data=data)
        return resp
    x = db.getallbs("car")
    output = dict()
    if x is not None:
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        out = json.dumps(x, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars", data=data)
        return resp
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars", data=data)
        return resp


########################################################################################################################
@app.route('/cars/Nearestcar', methods=['POST'])
def getlocationcars():
    token = flask.request.form["Token"]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 403,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/Nearestcar", data=data)
        return resp
    info = {
        "East": request.form["East"],
        "North": request.form["North"],
        "Number": request.form["Number"]
    }
    x = db.get_locations("car", info)
    output = dict()
    if x is not None:
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        out = json.dumps(x, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/Nearestcar", data=data)
        return resp
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/Nearestcar", data=data)
        return resp


########################################################################################################################
@app.route('/cars/UpdateCar', methods=['POST'])
def Updatecar():
    token = flask.request.form["Token"]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 403,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/UpdateCar", data=data)
        return resp
    info = {"Name": request.form['Name'],
            "Key": request.form["Key"]}

    x = db.UpdateCar(info)
    output = dict()
    if x is not None:
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        out = json.dumps(x, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/UpdateCar", data=data)
        return resp
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/cars/UpdateCar", data=data)
        return resp
