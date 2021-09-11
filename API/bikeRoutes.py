import flask
from API.routes import app
from flask import jsonify, request
import jwt
import datetime
from functools import wraps
import json
from DataBase import DataBase
from Models.Bike import validate

db = DataBase()
app.config["SECRET_KEY"] = "key"


# Token generation
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            txt = {"Action": 'Token is missing', "date": datetime.datetime.utcnow()}
            # jsontxt = json.dumps(txt)
            jsonFile = open("log.json", 'w')
            # jsonFile.append(jsontxt)
            jsonFile.close()

            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
            print(data)
        except:
            txt = {"Action": 'Token is Invalid', "date": datetime.datetime.utcnow()}
            # jsontxt = json.dumps(txt)
            jsonFile = open("log.json", 'w')
            # jsonFile.append(jsontxt)
            jsonFile.close()
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


#########################################################################################################################
@app.route('/')
def Welcome():
    return "Welcome to the Bike Server!"


##########################################################################################################################
@app.route('/bikes/Addbike', methods=['POST'])
def AddBike():
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
        info = {"East": request.form['East'],
                "North": request.form['North'],
                "Name": request.form['Name'],
                "Locked": request.form['Locked'],
                "Speed": request.form['Speed'],
                "Shared": request.form['Shared'],
                "IP": request.form['IP'],
                "Port": request.form['Port'],
                "Execute": request.form['Execute'],
                "Command": request.form['Command'],
                "Current_Network_Name": request.form['Current_Network_Name'],
                "Current_Network_Password": request.form['Current_Network_Password']}
        x = db.insertbike(info)
        output = dict()
        output['data'] = None
        if x is None:
            output['message'] = 'name is not unique'
            output['error'] = True
        else:
            output["data"] = x
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


##########################################################################################################################
@app.route('/bikes/getbike', methods=['POST'])  # here
def getBike():
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
    x = db.getbike(info)
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
        resp.headers['Output'] = out
        data = {'Response': out,
                'status': 500}
        return data


# ########################################################################################################################
@app.route('/bikes', methods=['POST'])
def getAllBikes():
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
    x = db.getallbike()
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


##########################################################################################################################
@app.route('/bikes/NearestBikes', methods=['POST'])  # and here
def get_location():
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
    x = db.get_locations(info)
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


##########################################################################################################################
@app.route('/bikes/UpdateBike', methods=['POST'])
def UpdateBike():
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
        "Name": request.form["Name"],
        "Locked": request.form["Locked"],
        "Speed": request.form["Speed"],
        "Shared": request.form["Shared"],
        "IP": request.form["IP"],
        "Port": request.form["Port"],
        "Execute": request.form["Execute"],
        "Command": request.form["Command"],
        "Current_Network_Name": request.form['Current_Network_Name'],
        "Current_Network_Password": request.form['Current_Network_Password']}
    x = db.UpdateBike(info)
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


##########################################################################################################################

@app.route('/bikes/updateCommand', methods=['POST'])
def updateCommand():
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
        "Name": request.form["Name"],
        "Command": request.form["Command"]
    }
    x = db.updateCommand(info)

    error = x["error"]
    message = x["message"]
    if not error:

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": x["message"]})
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


##########################################################################################################################
@app.route('/bikes/lockBike', methods=['POST'])
def updateLocked():
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
    x = db.lockBike(info)

    error = x["error"]
    message = x["message"]
    if not error:

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": x["message"]})
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


##########################################################################################################################
@app.route('/bikes/unlockBike', methods=['POST'])
def updateunLocked():
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
    x = db.unlockBike(info)

    error = x["error"]
    message = x["message"]
    if not error:

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": x["message"]})
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data


##########################################################################################################################

@app.route('/bikes/updateBike2', methods=['POST'])
def updateBike2():
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
        "Name": request.form["Name"],
        "North": request.form["North"],
        "East": request.form["East"],
        "Speed": request.form["Speed"]
    }
    x = db.updateBike2(info)

    error = x["error"]
    message = x["message"]
    if not error:

        out = json.dumps(message, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 200}
        return data
    else:
        out = json.dumps({"message": x["message"]})
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 500}
        return data
## VERY IMPORTANT NOTE, TELL ABDULRAHMAN THAT YOU CHANGED NEARESTBIKE AND GET BIKE TO POST!!

########## INTEGRATING WITH BACKEND
@app.route('/bikes/shareBike', methods=['POST'])
#@token_required
def sharebike():

    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("../log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    info = {
        "Name": request.form["Name"],
        "North": request.form["North"],
        "East": request.form["East"],
        "Speed": request.form["Speed"]
    }

    validated = db.shareBike(request.form)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
  
@app.route('/bikes/stopShareBike', methods=['POST'])
#@token_required
def stopsharebike():


    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("../log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    info = {
        "Name": request.form["Name"],
        "North": request.form["North"],
        "East": request.form["East"],
        "Speed": request.form["Speed"]
    }

    validated = db.stopShareBike(request.form)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
#####################################     LYDIA'S STUFF     #####################################

@app.route('/bikes/editPrice', methods=['POST'])
#@token_required
def editprice():

    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("../log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    info = {
        "Name": request.form["Name"],
        "North": request.form["North"],
        "East": request.form["East"],
        "Speed": request.form["Speed"]
    }


    validated = db.editPrice(request.form)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
      
        
@app.route('/bikes/getbikePrice/<name>', methods=['GET']) #here
def getBikePrice(name):
    
    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("../log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    info = {
        "Name": request.form["Name"],
        "North": request.form["North"],
        "East": request.form["East"],
        "Speed": request.form["Speed"]
    }


    x = db.getbikePrice(name)
    output = dict()
    
    if x is not None:
        output['data'] = x
        output['error'] = False
        return Response(
            response=json.dumps({
                "prices": x["message"]
            }),
            status=200,
            mimetype="application/json"
        )
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        return Response(
            response=json.dumps(output, default=str),
            status=500,
            mimetype="application/json"
        )
    
@app.route('/bikes/getBikeLocked/<name>', methods=['GET']) #here
def getBikeLocked(name):
    

    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("../log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
    info = {
        "Name": request.form["Name"],
        "North": request.form["North"],
        "East": request.form["East"],
        "Speed": request.form["Speed"]
    }


    x = db.getbikeLocked(name)
    output = dict()
    
    if x is not None:
        output['data'] = x
        output['error'] = False
        return Response(
            response=json.dumps({
                "Locked": x["message"]
            }),
            status=200,
            mimetype="application/json"
        )
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        return Response(
            response=json.dumps(output, default=str),
            status=500,
            mimetype="application/json"
        )
    
@app.route('/bikes/getBikeShared/<name>', methods=['GET']) #here
def getBikeShared(name):
    

    try:
        token = flask.request.form["Token"]
        data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
    except:
        txt = {"Action": 'Token is Invalid'}
        jsontxt = json.dumps(txt)
        jsonFile = open("../log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        out = json.dumps(txt, default=str)
        resp = flask.make_response(out)
        data = {'Response': out,
                'status': 403}
        return data
        
    info = {
        "Name": request.form["Name"],
        "North": request.form["North"],
        "East": request.form["East"],
        "Speed": request.form["Speed"]
    }
    


    x = db.getbikeShared(name)
    output = dict()
    
    if x is not None:
        output['data'] = x
        output['error'] = False
        return Response(
            response=json.dumps({
                "Shared": x["message"]
            }),
            status=200,
            mimetype="application/json"
        )
    else:
        output['data'] = None
        output['message'] = "False"
        output['error'] = True
        return Response(
            response=json.dumps(output, default=str),
            status=500,
            mimetype="application/json"
        )
