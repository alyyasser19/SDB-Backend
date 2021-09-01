import flask
import jwt
import requests

from routes import app
from flask import request, Response
from DataBase import DataBase
from Base_Station import validate
import json

db = DataBase()


########################################################################################################################
@app.route('/')
def Welcome():
    return "Welcome to the app!"


########################################################################################################################
@app.route('/infrastructures/addbasestaion', methods=['POST'])
def AddInfra():
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
        r = requests.post(url="http://localhost:5000/infrastructures/addbasestaion", data=data)
        return resp
    validated = validate(request.form)
    error = validated["error"]
    output = dict()
    if not error:
        info = {"North": request.form['North'],
                "East": request.form['East'],
                "IP": request.form['IP'],
                "Public_Key": request.form['Public_Key']}
        x = db.insertbs("basestation", info)
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
        r = requests.post(url="http://localhost:5000/infrastructures/addbasestaion", data=data)
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
        r = requests.post(url="http://localhost:5000/infrastructures/addbasestaion", data=data)
        return resp


########################################################################################################################
@app.route('/infrastructures/getbasestation', methods=['POST'])
def getInfra():
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
        r = requests.post(url="http://localhost:5000/infrastructures/getbasestation", data=data)
        return resp
    info = {
        "Name": request.form["Name"]
    }
    x = db.getbs("basestation", info)
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
        r = requests.post(url="http://localhost:5000/infrastructures/getbasestation", data=data)
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
        r = requests.post(url="http://localhost:5000/infrastructures/getbasestation", data=data)
        return resp


########################################################################################################################
@app.route('/infrastructures', methods=['POST'])
def getAllInfra():
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
        r = requests.post(url="http://localhost:5000/infrastructures", data=data)
        return resp
    x = db.getallbs("basestation")
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
        r = requests.post(url="http://localhost:5000/infrastructures", data=data)
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
        r = requests.post(url="http://localhost:5000/infrastructures", data=data)
        return resp


########################################################################################################################
@app.route('/infrastructures/Nearestbs', methods=['POST'])
def get_location_infra():
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
        r = requests.post(url="http://localhost:5000/infrastructures/Nearestbs", data=data)
        return resp
    info = {
        "East": request.form["East"],
        "North": request.form["North"],
        "Number": request.form["Number"]
    }
    x = db.get_locations("basestation", info)
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
        r = requests.post(url="http://localhost:5000/infrastructures/Nearestbs", data=data)
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
        r = requests.post(url="http://localhost:5000/infrastructures/Nearestbs", data=data)
        return resp
