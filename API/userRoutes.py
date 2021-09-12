import flask

from API.routes import app
from Models.User import registerValidate

from Models.User import signinValidate
from Models.User import emailCheck
from Models.User import getNumbers

from Models.User import editNum
from Models.User import removeNum

from Models.User import createRideDB

from Models.User import getUserBike
from Models.User import getCommand

from Models.User import removeCode

from Models.User import remBikeID

from Models.User import bikeID

from Models.User import getRides

from Models.User import validEmail

from Models.User import forgotPassword

from Models.User import addNum

from Models.User import changePassword

from Models.User import removeRideDB

from Models.User import tempBikeID

from Models.User import getUserTempBike

from Models.User import checkCode

from Models.User import changePwEz

from flask_bcrypt import Bcrypt

# from flask_mail import Mail
# , Message

import random
import string

import json

from flask import jsonify, request
import jwt
import datetime
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
    return "Welcome to the User Server!"


@app.route('/users/sendemail', methods=['POST'])
def sendEmail():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

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
    data = {'Response': out,
            'status': 200}
    return data


@app.route('/users/register', methods=['POST'])
def createUser():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    val = db.emailExists(request.form)

    info = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "password": request.form["password"]
    }

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
                    "numberOfRides": 0, "code": "", "balance": 0}

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
            data = {'Response': out,
                    'status': 200}
            return data
        else:
            out = json.dumps({"message": validated["message"]}, default=str)
            resp = flask.make_response(out)
            data = {'Response': out,
                    'status': 500}
            return data
    else:
        out = json.dumps({"message": val["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/getuserbike/<email>', methods=['POST'])
def getUserbike(email):
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    # msh bta5od 7aga mn forms.data

    validated = getUserBike(email)

    error = validated["error"]
    # message = validated["message"]
    if not error:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/getusertempbike/<email>', methods=['POST'])
def getUserTempBike(email):
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    validated = getUserTempBike(email)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/getcommand', methods=['POST'])
def getCMD():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"]
    }

    validated = getCommand(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/updatebikeid', methods=['POST'])
def updateBikeID():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"],
        "bikeID": request.form["bikeID"]
    }

    validated = bikeID(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/updatetempbikeid', methods=['POST'])
def updateTempBikeID():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"],
        "tempBikeID": request.form["tempBikeID"]
    }

    validated = tempBikeID(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/nullifybikeid', methods=['POST'])
def nullifyBikeID():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"]
    }

    validated = remBikeID(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


# EMERGENCY NUMBERS
@app.route('/users/addnumber', methods=['POST'])
def addNumber():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"],
        "numbers": request.form["numbers"]
    }

    validated = addNum(request.form)
    error = validated["error"]
    message = validated["message"]

    if (not error):
        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/editnumber', methods=['POST'])
def editNumber():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"],
        "numbers": request.form["numbers"],
        "numbers2": request.form["numbers2"]
    }

    validated = editNum(request.form)
    error = validated["error"]

    if (not error):

        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/removenumber', methods=['POST'])
def removeNumber():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"],
        "numbers": request.form["numbers"]
    }

    validated = removeNum(request.form)
    error = validated["error"]

    if (not error):

        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/gimmenums/<email>', methods=['POST'])
def getEmergencyNumbers(email):
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    dic = {"email": email}
    validated = getNumbers(dic)
    error = validated["error"]
    message = validated["message"]

    if (not error):

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


# EMERGENCY NUMBERS   


# RIDE ROUTES

# create a new ride with (ride number, history, startDate, endDate, startTime, endTime)
@app.route('/users/createRide', methods=['POST'])
def createRide():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    # email_func

    info = {
        "email": request.form["email"],
        "history": request.form["history"],
        "startDate": request.form["startDate"],
        "endDate": request.form["endDate"],
        "startTime": request.form["startTime"],
        "endTime": request.form["endTime"]
    }

    validated = createRideDB(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/removeride', methods=['POST'])
def removeRide():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    # email_func

    info = {
        "email": request.form["email"],
        "rideNo": request.form["rideNo"]
    }

    validated = removeRideDB(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps("Ride Removed!", default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data

    # get all rides    


@app.route('/users/getrides/<email>', methods=['POST'])
def getRide(email):
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    # email_func
    dic = {"email": email}
    validated = getRides(dic)
    error = validated["error"]

    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data

    # get 1 ride with rideNo


# RIDE ROUTES


@app.route('/users/checkemail', methods=['POST'])
def checkEmail():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    # email_func

    info = {
        "email": request.form["email"]
    }

    validated = emailCheck(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/emailVal', methods=['POST'])
def emailVall():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"]
    }

    validated = validEmail(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data


###############################################################################################
#################################### FORGOT PASSWORD STUFF ####################################

@app.route('/users/forgotpassword', methods=['POST'])
def forgotPW():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"]
    }

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
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/checkcode', methods=['POST'])
def checkcode():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    # bta5od email wel entered code mn el user

    info = {
        "email": request.form["email"],
        "code": request.form["code"]
    }

    validated = checkCode(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/changepwez', methods=['POST'])
def changePWEZ():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    # bta5od email wel entered code mn el user

    info = {
        "email": request.form["email"],
        "newpassword": request.form["newpassword"]
    }

    validated = changePwEz(request.form)
    error = validated["error"]

    if not error:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


###############################################################################################
################################## END FORGOT PASSWORD STUFF ##################################

@app.route('/users/removecode', methods=['POST'])
def removecode():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"]
    }

    validated = removeCode(request.form)
    error = validated["error"]

    if (not error):
        out = json.dumps(request.form, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/login', methods=['POST'])
def login():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

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
        data = {'Response': out,
                'status': 200}
        return data
    else:
        txt = {"Action": 'Token could not be verified'}
        # jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        # jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/changepw', methods=['POST'])
def changepw():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"],
        "password": request.form["password"],
        "newpassword": request.form["newpassword"]
    }

    validated = changePassword(request.form)
    error = validated["error"]
    msg = validated["message"]
    if (not error):

        # return "Sent"

        out = json.dumps("Password has changed", default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data


########### Newest stuff


@app.route('/users/getname/<email>', methods=['POST'])
def getname(email):
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("/log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    validated = db.getName(email)
    error = validated["error"]

    if (not error):
        out = json.dumps({
            "firstName": validated["firstName"],
            "lastName": validated["lastName"]
        }, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/getbalance/<email>', methods=['POST'])
def getbalance(email):
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("/log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    validated = db.getBalance(email)
    error = validated["error"]

    if (not error):
        out = json.dumps({
            "balance": validated["balance"]
        }, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/nullifytempbikeid', methods=['POST'])
def nullifyTempBikeID():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("/log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "email": request.form["email"]
    }

    validated = db.removeTempBikeID(request.form)

    error = validated["error"]
    message = validated["message"]
    if (not error):
        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data


@app.route('/users/addtobalance', methods=['POST'])  ## needs bike name (Name) and money number (money)
def addtobalance():
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("/log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data

    info = {
        "Name": request.form["Name"],
        "money": request.form["money"]
    }

    validated = db.addToBalance(request.form)

    error = validated["error"]
    # message = validated["message"]
    if (not error):
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": validated["message"]}, default=str)
        resp = flask.make_response(out)
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data
