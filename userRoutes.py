import flask
import requests

from routes import app
from flask import Response
from User import registerValidate

from User import signinValidate
from User import emailCheck
from User import getNumbers

from User import editNum
from User import removeNum

from User import createRideDB

from User import getUserBike
from User import getCommand

from User import removeCode

from User import remBikeID

from User import bikeID

from User import getRides

from User import validEmail

from User import forgotPassword

from User import addNum

from User import changePassword

from User import removeRideDB

from User import tempBikeID

from User import getUserTempBike

from User import checkCode

from User import changePwEz

from flask_bcrypt import Bcrypt

# from flask_mail import Mail
# , Message

import random
import string

import json

from flask import jsonify, request
import jwt
import datetime
import os
from functools import wraps

app.config['SECRET_KEY'] = "key"

from DataBase import DataBase

db = DataBase()

bcrypt = Bcrypt(app)


# @app.route('/users/<id>', methods=['GET'])
# def getUser(id):
# return id


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            txt = {"Action": 'Token is missing', "date": datetime.datetime.utcnow()}
            #          jsontxt = json.dumps(txt)
            jsonFile = open("log.json", 'w')
            #  jsonFile.write(jsontxt)
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
def welcome():
    return "Welcome to the app!"


@app.route('/users/sendemail', methods=['POST'])
def sendEmail():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/sendemail", data=data)
        return resp

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'bikeroonsApp@gmail.com'
    app.config['MAIL_PASSWORD'] = "Ll1234567"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    #  mail = Mail(app)

    #  msg = Message('Hello', sender = 'BikeroonsApp@gmail.com', recipients = ['lydiay711@gmail.com'])
    # msg.body = "This is the email body"
    # mail.send(msg)
    out = json.dumps("Sent", default=str)
    resp = flask.make_response(out)
    resp.headers['Output'] = out
    data = {'Response': out,
            'status': 200,
            'token': token,
            'state': 'received'}
    r = requests.post(url="http://localhost:5000/users/sendemail", data=data)
    return resp


@app.route('/users/register', methods=['POST'])
def createUser():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/register", data=data)
        return resp
    val = db.emailExists(request.form)

    if not val["error"]:

        validated = registerValidate(request.form)

        error = validated["error"]
        message = validated["message"]

        if (not error):

            hashedpw = validated["newpw"]
            # info = {"fname": request.form['fname'], "lname": request.form['lname'], "email": request.form['email'],"password": request.form['password'],"bikeID":None,"numbers":[],"rides":[{"rideNo":0},{"history":[]},{"startDate":""},{"endDate":""},{"startTime":""},{"endTime":""}]}
            # info = {"fname": request.form['fname'], "lname": request.form['lname'], "email": request.form['email'],"password": request.form['password'],"bikeID":None,"numbers":[],"rides":[]}
            info = {"fname": request.form['fname'], "lname": request.form['lname'], "email": request.form['email'],
                    "password": hashedpw, "bikeID": "", "tempBikeID": "", "numbers": [], "rides": [],
                    "numberOfRides": 0, "code": ""}

            db.araf(info)

            # app.config['MAIL_SERVER']='smtp.gmail.com'
            # app.config['MAIL_PORT'] = 465
            # app.config['MAIL_USERNAME'] = 'bikeroonsApp@gmail.com'
            # app.config['MAIL_PASSWORD'] = "Ll1234567"
            # app.config['MAIL_USE_TLS'] = False
            # app.config['MAIL_USE_SSL'] = True

            # mail = Mail(app)

            # msg = Message('Welcome to Bikeroons!', sender = 'BikeroonsApp@gmail.com', recipients = [request.form['email']])
            # msg.body = f"We are thrilled to have you become a member of the Bikeroons community\nYour Login information is:\n\nE-mail: {request.form['email']}\nPassword: {request.form['password']} "
            # mail.send(msg)
            # return "Sent"

            out = json.dumps(message, default=str)
            resp = flask.make_response(out)
            resp.headers['Output'] = out
            data = {'Response': out,
                    'status': 200,
                    'token': token,
                    'state': 'received'}
            r = requests.post(url="http://localhost:5000/users/register", data=data)
            return resp
        else:
            out = json.dumps({"message": validated["message"]}, default=str)
            resp = flask.make_response(out)
            resp.headers['Output'] = out
            data = {'Response': out,
                    'status': 500,
                    'token': token,
                    'state': 'received'}
            r = requests.post(url="http://localhost:5000/users/register", data=data)
            return resp
    else:
        out = json.dumps({"message": val["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/register", data=data)
        return resp


@app.route('/users/getuserbike/<email>', methods=['POST'])
def getUserbike(email):
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/getuserbike/<email>", data=data)
        return resp
    validated = getUserBike(email)

    error = validated["error"]
    # message = validated["message"]
    if not error:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getuserbike/<email>", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getuserbike/<email>", data=data)
        return resp


@app.route('/users/getusertempbike/<email>', methods=['POST'])
def getUserTempBike(email):
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/getusertempbike/<email>", data=data)
        return resp
    validated = getUserTempBike(email)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getusertempbike/<email>", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getusertempbike/<email>", data=data)
        return resp


@app.route('/users/getcommand', methods=['POST'])
def getCMD():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/getcommand", data=data)
        return resp
    validated = getCommand(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getcommand", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getcommand", data=data)
        return resp


@app.route('/users/updatebikeid', methods=['POST'])
def updateBikeID():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/updatebikeid", data=data)
        return resp
    validated = bikeID(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/updatebikeid", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/updatebikeid", data=data)
        return resp


@app.route('/users/updatetempbikeid', methods=['POST'])
def updateTempBikeID():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/updatetempbikeid", data=data)
        return resp
    validated = tempBikeID(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/updatetempbikeid", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/updatetempbikeid", data=data)
        return resp


@app.route('/users/nullifybikeid', methods=['POST'])
def nullifyBikeID():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/nullifybikeid", data=data)
        return resp
    validated = remBikeID(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/nullifybikeid", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/nullifybikeid", data=data)
        return resp


# EMERGENCY NUMBERS
@app.route('/users/addnumber', methods=['POST'])
def n5alas():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/addnumber", data=data)
        return resp
    validated = addNum(request.form)
    error = validated["error"]
    message = validated["message"]

    if (not error):
        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/addnumber", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/addnumber", data=data)
        return resp


@app.route('/users/editnumber', methods=['POST'])
def editNumber():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/editnumber", data=data)
        return resp
    validated = editNum(request.form)
    error = validated["error"]

    if (not error):

        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/editnumber", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/editnumber", data=data)
        return resp


@app.route('/users/removenumber', methods=['POST'])
def removeNumber():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/removenumber", data=data)
        return resp
    validated = removeNum(request.form)
    error = validated["error"]

    if (not error):

        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/removenumber", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/removenumber", data=data)
        return resp


@app.route('/users/gimmenums/<email>', methods=['POST'])
def getEmergencyNumbers(email):
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/gimmenums/<email>", data=data)
        return resp
    dic = {"email": email}
    validated = getNumbers(dic)
    error = validated["error"]
    message = validated["message"]

    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/gimmenums/<email>", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/gimmenums/<email>", data=data)
        return resp


# EMERGENCY NUMBERS   


# RIDE ROUTES

# create a new ride with (ride number, history, startDate, endDate, startTime, endTime)
@app.route('/users/createRide', methods=['POST'])
def createRide():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/createRide", data=data)
        return resp
    # email_func
    validated = createRideDB(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/createRide", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/createRide", data=data)
        return resp


@app.route('/users/removeride', methods=['POST'])
def removeRide():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/removeride", data=data)
        return resp
    # email_func
    validated = removeRideDB(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps("Ride Removed!", default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/removeride", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/removeride", data=data)
        return resp

    # get all rides    


@app.route('/users/getrides/<email>', methods=['POST'])
def getRide(email):
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/getrides/<email>", data=data)
        return resp
    # email_func
    dic = {"email": email}
    validated = getRides(dic)
    error = validated["error"]

    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getrides/<email>", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/getrides/<email>", data=data)
        return resp

    # get 1 ride with rideNo


# RIDE ROUTES


@app.route('/users/checkemail', methods=['POST'])
def checkEmail():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/checkemail", data=data)
        return resp
    # email_func
    validated = emailCheck(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/checkemail", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/checkemail", data=data)
        return resp


@app.route('/users/emailVal', methods=['POST'])
def emailVall():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/emailVal", data=data)
        return resp
    validated = validEmail(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/emailVal", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/emailVal", data=data)
        return resp


###############################################################################################
#################################### FORGOT PASSWORD STUFF ####################################

@app.route('/users/forgotpassword', methods=['POST'])
def forgotPW():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/forgotpassword", data=data)
        return resp
    letters = string.ascii_letters
    code = ''.join(random.choice(letters) for i in range(4))

    validated = forgotPassword(request.form, code)
    error = validated["error"]

    if (not error):

        print(code)

        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'bikeroonsApp@gmail.com'
        app.config['MAIL_PASSWORD'] = "Ll1234567"
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True

        #  mail = Mail(app)

        #  msg = Message('Code to change password', sender = 'BikeroonsApp@gmail.com', recipients = [request.form['email']])
        #   msg.body = "You have requested to change your password. To proceed with the process, enter the following code in the space provided in Bikeroons: "+code
        #  mail.send(msg)

        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/forgotpassword", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/forgotpassword", data=data)
        return resp


@app.route('/users/checkcode', methods=['POST'])
def checkcode():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/checkcode", data=data)
        return resp
    # bta5od email wel entered code mn el user

    validated = checkCode(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/checkcode", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/checkcode", data=data)
        return resp


@app.route('/users/changepwez', methods=['POST'])
def changePWEZ():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/changepwez", data=data)
        return resp
    # bta5od email wel entered code mn el user

    validated = changePwEz(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/changepwez", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/changepwez", data=data)
        return resp


###############################################################################################
################################## END FORGOT PASSWORD STUFF ##################################

@app.route('/users/removecode', methods=['POST'])
def removecode():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/removecode", data=data)
        return resp
    validated = removeCode(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/removecode", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/removecode", data=data)
        return resp


@app.route('/users/login', methods=['POST'])
def login():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/login", data=data)
        return resp
    validated = signinValidate(request.form)
    error = validated["error"]

    message = validated["message"]
    auth = request.form["email"]
    if (not error):

        tokenLogin = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], "HS256")
        txt = {"Action": 'Token was authorized', "User": auth}
        # jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        # jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps({'LoginToken': tokenLogin}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/login", data=data)
        return resp
    else:

        txt = {"Action": 'Token could not be verified'}
        # jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        # jsonFile.write(jsontxt)
        jsonFile.close()

        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/login", data=data)
        return resp


@app.route('/users/changepw', methods=['POST'])
def changepw():
    token = flask.request.form["token"]
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
        r = requests.post(url="http://localhost:5000/users/changepw", data=data)
        return resp
    validated = changePassword(request.form)
    error = validated["error"]
    msg = validated["message"]
    if (not error):

        # return "Sent"

        out = json.dumps("Password has changed", default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 200,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/changepw", data=data)
        return resp
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500,
                'token': token,
                'state': 'received'}
        r = requests.post(url="http://localhost:5000/users/changepw", data=data)
        return resp

# @app.route('/users/getspeed', methods=['GET'])
# def getSpeed():
#   validated = loginValidate(request.form)
#  error = validated["error"]
# if(not error):
#    return Response(
#       response=json.dumps(request.form),
#      status=200,
#     mimetype="application/json"
# )
# else:
#   return Response(
#      response=json.dumps({
#         "message": validated["message"]
#    }),
#   status=500,
#   mimetype="application/json"
# )
