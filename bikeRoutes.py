import flask

from routes import app
from flask import request, Response
import json
from DataBase import DataBase
from Bike import validate
db = DataBase()

#########################################################################################################################
@app.route('/')
def Welcome():
    return "Welcome to the app!"
##########################################################################################################################
@app.route('/bikes/Addbike', methods=['POST'])
def AddBike():
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
                "Execute":request.form['Execute'],
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
        return Response(
            response=json.dumps(output, default=str),
            status=200,
            mimetype="application/json"
        )
    else:
        x = None
        output['data'] = x
        output['message'] = validated["message"]
        output['error'] = True
        return Response(
            response=json.dumps(output, default=str),
            status=500,
            mimetype="application/json"
        )
##########################################################################################################################
@app.route('/bikes/getbike', methods=['POST']) #here
def getBike():
    info = {
        "Name": request.form["Name"]
    }
    x = db.getbike(info)
    output = dict()
    headers = flask.request.headers
    if x is not None and headers["sender"] == "main":
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        return Response(
            response=json.dumps(output, default=str),
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
##########################################################################################################################
@app.route('/bikes', methods=['GET'])
def getAllBikes():
    x = db.getallbike()
    output = dict()
    if x is not None:
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        return Response(
            response=json.dumps(x, default=str),
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
##########################################################################################################################
@app.route('/bikes/NearestBikes', methods=['POST']) #and here
def get_location():
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
        return Response(
            response=json.dumps(output, default=str),
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
##########################################################################################################################
@app.route('/bikes/UpdateBike', methods=['POST'])
def UpdateBike():
    info = {
        "East": request.form["East"],
        "North": request.form["North"],
        "Name": request.form["Name"],
        "Locked": request.form["Locked"],
        "Speed": request.form["Speed"],
        "Shared": request.form["Shared"],
        "IP": request.form["IP"],
        "Port": request.form["Port"],
        "Execute":request.form["Execute"],
        "Command":request.form["Command"],
        "Current_Network_Name": request.form['Current_Network_Name'],
        "Current_Network_Password": request.form['Current_Network_Password']}
    x = db.UpdateBike(info)
    output = dict()
    if x is not None:
        output['data'] = x
        output['message'] = 'Success'
        output['error'] = False
        return Response(
            response=json.dumps(x, default=str),
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
##########################################################################################################################

@app.route('/bikes/updateCommand', methods=['POST'])
def updateCommand():
    info = {
        "Name":request.form["Name"],
        "Command": request.form["Command"]
    }
    x = db.updateCommand(info)
      
    error = x["error"]
    message = x["message"]
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
                "message": x["message"]
            }),
            status=500,
            mimetype="application/json"
        )
##########################################################################################################################
@app.route('/bikes/lockBike', methods=['POST'])
def updateLocked():
    info = {
        "Name":request.form["Name"]
    }
    x = db.lockBike(info)
      
    error = x["error"]
    message = x["message"]
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
                "message": x["message"]
            }),
            status=500,
            mimetype="application/json"
        )
##########################################################################################################################
@app.route('/bikes/unlockBike', methods=['POST'])
def updateunLocked():
    info = {
        "Name":request.form["Name"]
    }
    x = db.unlockBike(info)
      
    error = x["error"]
    message = x["message"]
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
                "message": x["message"]
            }),
            status=500,
            mimetype="application/json"
        )
##########################################################################################################################

@app.route('/bikes/updateBike2', methods=['POST'])
def updateBike2():
    info = {
        "Name":request.form["Name"],
        "North": request.form["North"],
        "East":request.form["East"],
        "Speed":request.form["Speed"]
    }
    x = db.updateBike2(info)
      
    error = x["error"]
    message = x["message"]
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
                "message": x["message"]
            }),
            status=500,
            mimetype="application/json"
        )
## VERY IMPORTANT NOTE, TELL ABDULRAHMAN THAT YOU CHANGED NEARESTBIKE AND GET BIKE TO POST!!