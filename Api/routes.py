import flask
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config["DEBUG"] = True
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

from . import bikeApi
from . import userApi


@app.route('/test/<string>', methods=['GET'])
# @cache.cached(timeout=120)
def test(string):
    print("test")
    # print(f"/test/{string}", flask.request.form)
    helper(string, flask.request.form)
    s=f"test_{flask.request.form['k1']}"
    return s


@cache.memoize(120)
def helper(string, form):
    print("helper",string,form)
    return ""