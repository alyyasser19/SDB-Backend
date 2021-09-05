import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import requests
from flask_caching import Cache
config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/', methods=['GET'])
def wakeup():
    url = 'https://sdb-app-main.herokuapp.com/' 
    requests.get(url)
    requests.post(url, data="")
    url1 = 'https://sdb-app-bike.herokuapp.com/'
    requests.get(url1)
    requests.post(url1, data="")
    requests.get(url)
    requests.post(url, data="")
    url2 = 'https://sdb-app-carinfra.herokuapp.com/'
    requests.get(url2)
    requests.post(url2, data="")
    requests.get(url)
    requests.post(url, data="")
    url3 = 'https://sdb-app-users.herokuapp.com/'
    requests.get(url3)
    requests.post(url3, data="")
    requests.get(url)
    requests.post(url, data="")


scheduler = BackgroundScheduler()
scheduler.add_job(func=wakeup, trigger="interval", minutes=30)
scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True)
