#!/usr/bin/python3
""" Locations Route module """

from api.v1.auth_middleware import admin_token_required, token_required
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

from models import storage
from models.location import Location

@app_views.route('/locations', methods=['GET'], strict_slashes=False)
@token_required
def get_all_locations(current_user):
    """ get all locations """
    all_locations = storage.all(Location)
    all_locations = [location.to_dict() for location in all_locations.values()]
    return jsonify(all_locations)

@app_views.route('/locations/<location_id>', methods=['GET'], strict_slashes=False)
@token_required
def get_location(current_user, location_id):
    """get a location by id"""
    location = storage.get(Location, location_id)

    if not location:
        abort(404)

    return jsonify(location.to_dict()), 200

@app_views.route('/locations', methods=['POST'], strict_slashes=False)
@admin_token_required
def post_location(current_user):
    """creates a Location"""
    try:
        if not request.get_json():
            return {
            "status": "error",
            "data": None,
            "message": "Not a JSON"
        }, 400

        if 'name' not in request.get_json():
            return {
            "status": "error",
            "data": None,
            "message": "Missing Location Name"
        }, 400

        data = request.get_json()
        instance = Location(**data)
        instance.save()
        return make_response(jsonify({"status": "success","data": instance.to_dict(), "message": "Location Added"}), 201)
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }, 500

@app_views.route('/locations/<location_id>', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_location(current_user, location_id):
    """ deletes a location with location_id """
    try:
        location = storage.get(Location, location_id)

        if not location:
            return {
            "status": "error",
            "data": None,
            "message": "Invalid Location ID"
            }, 404

        storage.delete(location)

        storage.save()
        return make_response(jsonify({
            "status": "success",
            "data": {},
            "message": "Record Deleted"}), 200)
        
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }, 500

@app_views.route('/locations/<location_id>', methods=['PUT'], strict_slashes=False)
@token_required
def put_location(current_user, location_id):
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
    