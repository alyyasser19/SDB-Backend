import flask
import jwt

from API.routes import app
from flask import request
from DataBase import DataBase
from Models.Base_Station import validate
import json

db = DataBase()


########################################################################################################################
@app.route('/')
def Welcome():
    return "Welcome to the CarInfra Server!"


########################################################################################################################
@app.route('/infrastructures/addbasestation', methods=['POST'])
def AddInfra():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.append(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    validated = validate(request.form)
    error = validated["error"]
    output = dict()
    if not error:
        info = {"Name": request.form['Name'],
                "North": request.form['North'],
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
        data = {'Response': out,
                'status': 200}
        return data
    else:
        x = None
        output['data'] = x
        output['message'] = validated["message"]
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


########################################################################################################################
@app.route('/infrastructures/getbasestation', methods=['POST'])
def getInfra():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.append(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
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
        data = {'Response': out,
                'status': 200}
        return data
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


########################################################################################################################
@app.route('/infrastructures', methods=['POST'])
def getAllInfra():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.append(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    x = db.getallbs("basestation")
    output = dict()
    if x is not None:
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        out = json.dumps(x, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


########################################################################################################################
@app.route('/infrastructures/Nearestbs', methods=['POST'])
def get_location_infra():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.append(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
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
        data = {'Response': out,
                'status': 200}
        return data
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        out = json.dumps(output, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data
