#!/usr/bin/python3
""" Index module """

from flask import jsonify
from sqlalchemy import false
from api.v1.views import app_views
from models.engine.db_storage import classes
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_number():
    """ Retrieves the number of each objects by type """

    obj_dict = {}
    for key, val in classes.items():
        obj_dict[key] = storage.count(val)

    return jsonify(obj_dict)
