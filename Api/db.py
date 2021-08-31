import pymongo
import Config
import urllib
from pymongo.errors import CollectionInvalid
from collections import OrderedDict


class DataBase:
    def __init__(self):
        client = pymongo.MongoClient(f"mongodb+srv://{Config.DB_USER}:{urllib.parse.quote(Config.DB_PASS)}"
                                     f"@cluster0.ibr9d.mongodb.net/{Config.DB_NAME}?retryWrites=true&w=majority")
        self.db = client.users
        print("connected to the DB!")


user_schema = {
    'card_number': {
        'type': 'string',
        'minlength': 16,
        'required': True,
    },
    'expiry_date': {
        'type': 'datetime',
        'required': True,
    },
    'cardholder_name': {
        'type': 'string',
        "required": False,
    },
    'ccv': {
        'type': 'int',
        'minlength': 3,
        'required': True,
    }
}

collection = 'Userinformation'
validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
required = []

for field_key in user_schema:
    field = user_schema[field_key]
    properties = {'bsonType': field['type']}
    minimum = field.get('minlength')

    if type(minimum) == int:
        properties['minimum'] = minimum

    if field.get('required') is True: required.append(field_key)

    validator['$jsonSchema']['properties'][field_key] = properties

if len(required) > 0:
    validator['$jsonSchema']['required'] = required

query = [('collMod', collection),
         ('validator', validator)]

try:
    client.create_collection(collection)
except CollectionInvalid:
    pass

command_result = client.command(OrderedDict(query))