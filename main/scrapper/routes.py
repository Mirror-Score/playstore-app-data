from flask import Blueprint, jsonify, request
from main import cache

from .utils import get_data

scrapper = Blueprint("scrapper", __name__)


@scrapper.route("/", methods=["GET"])
@cache.cached(query_string=True)
def get_playstore_data():
    id = request.args.get("id")
    keys = request.args.get("only")
    data = {"message": "Please add id as query parameter"}
    if id:
        data = get_data(id, keys)
    return jsonify(data)
