import os

if "vars.py" in os.listdir():
    from vars import *  # local server environment variables
else:
    DB_USER = os.environ["dbUserName"]
    DB_PASS = os.environ["dbPassword"]
    DB_NAME = os.environ["dbName"]    
