import json

from flask import Flask, jsonify, request, make_response
import jwt
import datetime
import os
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            txt = {"Action": 'Token is missing', "date": datetime.datetime.utcnow()}
            jsontxt = json.dumps(txt)
            jsonFile = open("API/log.json", 'w')
            jsonFile.write(jsontxt)
            jsonFile.close()

            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
            print(data)
        except:
            txt = {"Action": 'Token is Invalid', "date": datetime.datetime.utcnow()}
            jsontxt = json.dumps(txt)
            jsonFile = open("API/log.json", 'w')
            jsonFile.write(jsontxt)
            jsonFile.close()
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with valid tokens.'})


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'mamamia':
        print(auth.username)
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], "HS256")
        txt = {"Action": 'Token was authorized', "User": auth.username, }
        jsontxt = json.dumps(txt)
        jsonFile = open("API/log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()
        return jsonify({'token': token})
    else:
        txt = {"Action": 'Token could not be verified'}
        jsontxt = json.dumps(txt)
        jsonFile = open("API/log.json", 'w')
        jsonFile.write(jsontxt)
        jsonFile.close()

        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)

