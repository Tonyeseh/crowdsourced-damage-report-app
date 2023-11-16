#!/usr/bin/python3
""" Locations Route module """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

from models import storage
from models.location import Location

@app_views.route('/locations', methods=['GET'], strict_slashes=False)
def get_all_locations():
    """ get all locations """
    all_locations = storage.all(Location)
    all_locations = [location.to_dict() for location in all_locations.values()]
    return jsonify(all_locations)

@app_views.route('/locations/<location_id>', methods=['GET'], strict_slashes=False)
def get_location(location_id):
    """get a location by id"""
    location = storage.get(Location, location_id)

    if not location:
        abort(404)

    return jsonify(location.to_dict()), 200

@app_views.route('/locations', methods=['POST'], strict_slashes=False)
def post_location():
    """creates a Location"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Location(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/locations/<location_id>', methods=['DELETE'], strict_slashes=False)
def delete_location(location_id):
    """ deletes a location with location_id """
    location = storage.get(Location, location_id)

    if not location:
        abort(404)

    storage.delete(location)

    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/locations/<location_id>', methods=['PUT'], strict_slashes=False)
def put_location(location_id):
    """ updates a location """
    location = storage.get(Location, location_id)

    if not location:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'updated_at', 'created_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(location, key, value)

    storage.save()

    return make_response(jsonify(location.to_dict()), 200)
    