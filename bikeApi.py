from routes import app
from flask import redirect,request
from app import Config
import requests

@app.route('/bikes/<id>', methods=['GET'])
def getBike(id):
    return redirect(f"{Config.BIKE_PORT}/{id}")

@app.route('/bikes/create', methods=['POST'])
def createBike():
    r = requests.post(f"{Config.BIKE_PORT}/create",request.form)
    return r.json() 