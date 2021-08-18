from .routes import app
from flask import request, Response
from Main import db
from Models.Base_Station import validate
import json
########################################################################################################################
@app.route('/infrastructures/addbasestaion', methods=['POST'])
def AddInfra():
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
        return Response(
            response=json.dumps(output,default=str),
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
@app.route('/infrastructures/getbasestation', methods=['GET'])
def getInfra():
    info = {
        "Name": request.form["Name"]
    }
    x = db.getbs("basestation", info)
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
@app.route('/infrastructures', methods=['GET'])
def getAllInfra():
    x = db.getallbs("basestation")
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
@app.route('/infrastructures/Nearestbs', methods=['GET'])
def get_location_infra():
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