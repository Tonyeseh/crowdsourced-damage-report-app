#!/usr/bin/python3
""" Infrastructures Route module """

from flask import abort, jsonify, make_response, request
from models import storage
from models.infrastructure import Infrastructure
from models.location import Location

from api.v1.views import app_views
from api.v1.auth_middleware import token_required


# helper functions
def return_dict(infras: Infrastructure):
    """ return dict with more information """
    infras.location_name = infras.location.name
    infras = infras.to_dict()

    remove_class(infras)
    return infras

def remove_class(infras):
    """removes location class"""
    del infras['location']


# get all
@app_views.route('/infrastructures', methods=['GET'], strict_slashes=False)
def get_infrastructures():
    """ gets all infrastructures """
    all_infras = storage.all(Infrastructure)
    
    if not all_infras:
        abort(404)

    all_infras = [return_dict(infras) for infras in all_infras.values()]

    return jsonify(all_infras)

# get one
@app_views.route('/infrastuctures/<infras_id>', methods=['GET'], strict_slashes=False)
def get_infrastructure(infras_id):
    """gets an infrastucture """
    infras = storage.get(Infrastructure, infras_id)

    if not infras:
        abort(404)

    return jsonify(infras.to_dict())

# get from specific location
@app_views.route('/locations/<location_id>/infrastructures', methods=['GET'], strict_slashes=False)
def get_infrastructures_from_loc(location_id):
    """get infrastructure from location """
    location = storage.get(Location, location_id)

    if not location:
        abort(400, description="Location doesn't exist")

    loc_infras = [return_dict(loc) for loc in location.infrastructures]

    return jsonify(loc_infras)

# post
@app_views.route('locations/<location_id>/infrastructures', methods=['POST'], strict_slashes=False)
@token_required
def post_infrastructure(current_user, location_id):
    """ add an Infrastructure """
    if not request.get_json():
        abort(400, description="Not a JSON")

    print("location", location_id)

    location = storage.get(Location, location_id)
    if not location:
        abort(404)

    infras_attr = ['name', 'description']
    for val in infras_attr:
        if val not in request.get_json():
            abort(400, '{val} is missing'.format(val=val))

    data = request.get_json()
    instance = Infrastructure(**data)
    instance.location_id = location.id
    instance.save()

    return make_response(return_dict(instance), 201)
    

# put
@app_views.route('/infrastuctures/<infras_id>', methods=['PUT'], strict_slashes=False)
def put_infrastructure(infras_id):
    """updates an infrastructure info"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    infras = storage.get(Infrastructure, infras_id)
    if not infras:
        abort(404)

    ignore = ['id', 'updated_at', 'created_at']

    data = request.get_json()
    for key, value in infras.items():
        if key not in ignore:
            setattr(infras, key, value)
    storage.save()

    return make_response(jsonify(return_dict(infras)), 200)

# delete
@app_views.route('/infrastructures/<infras_id>', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_infrastructure(current_user, infras_id):
    """deletes an infrastructure instance"""
    infras = storage.get(Infrastructure, infras_id)

    if not infras:
        abort(404, description="Invalid Infrastructure ID")

    storage.delete(infras)
    storage.save()

    return jsonify({})
