from routes import app
from flask import request,redirect
from app import Config
import requests

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    return redirect(f"{Config.USER_PORT}/{id}")


@app.route('/users/create', methods=['Post'])
def createUser():
    r = requests.post(f"{Config.USER_PORT}/create",request.form)
    return r.json() 

@app.route('/users/login', methods=['GET'])
def login():
    r = requests.get(f"{Config.USER_PORT}/login",request.form)
    return r.json() 
