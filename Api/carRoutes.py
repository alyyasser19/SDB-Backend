from .routes import app
from flask import request, Response
from Main import db
from Models.Cars import validate
import json
########################################################################################################################
@app.route('/cars/addcar', methods=['POST'])
def AddCar():
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
########################################################################################################################
@app.route('/cars/getcar', methods=['GET'])
def getCar():
    info = {
        "Name": request.form["Name"]
    }
    x = db.getbs("car", info)
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
########################################################################################################################
@app.route('/cars', methods=['GET'])
def getAllCars():
    x = db.getallbs("car")
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
########################################################################################################################
@app.route('/cars/Nearestcar', methods=['GET'])
def getlocationcars():
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
 ########################################################################################################################   
@app.route('/cars/UpdateCar', methods=['POST'])
def Updatecar():
    info = {    "Name": request.form['Name'],
                "Key": request.form["Key"]}
    
    x = db.UpdateCar(info)
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