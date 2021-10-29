from flask import Flask, jsonify, request
from flask_caching import Cache

from main.scrapper import get_data

config = {"DEBUG": False, "CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}

CACHE_TIMEOUT = 60 * 60  # one hour


app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


@app.route("/")
@cache.cached(timeout=CACHE_TIMEOUT, query_string=True)
def hello_world():
    id = request.args.get("id")
    data = {}
    if id:
        data = get_data(id)

    return jsonify(data)
