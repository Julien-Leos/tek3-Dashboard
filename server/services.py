import json

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_api import status

from firebase import database
import app

services_page = Blueprint('services_page', __name__)


@services_page.route('/services', defaults={'serviceName': None}, methods=["GET"])
@services_page.route('/services/<serviceName>', methods=["GET"])
def services(serviceName):
    with open('about.json', 'r') as json_file:
        data = json.load(json_file)["server"]["services"]

    if request.method == "GET" and not serviceName:
        return List(data)
    elif request.method == "GET" and serviceName:
        return Get(data, serviceName.lower())


def List(data):
    return jsonify({"message": "Services successfully getted", "data": {"services": data}}), status.HTTP_200_OK


def Get(data, serviceName):
    for service in data:
        if service["name"] == serviceName:
            return jsonify({"message": "Service '" + serviceName + "' successfully getted", "data": {"services": service}}), status.HTTP_200_OK
    return jsonify({"message": "Error: Service '" + serviceName + "' do not exist."}), status.HTTP_400_BAD_REQUEST
