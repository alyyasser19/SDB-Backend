from .routes import app
from flask import request,Response
import json

@app.route('/admins/<id>', methods=['GET'])
def getAdmin(id):
    return Response(
        response=json.dumps({
            "_id":id
        }),
        status=200,
        mimetype="application/json"
    )
