from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True

from API import userRoutes
from API import adminRoutes

