#!/usr/bin/python3
""" Facilities Route module """

from api.v1.auth_middleware import token_required
from models import storage
from models.infrastructure import Infrastructure
from models.facility import Facility
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views

# get all facilities
@app_views.route('/facilities', methods=['GET'], strict_slashes=False)
@token_required
def get_facilities(current_user):
    """ gets all facilities """
    all_facilities = storage.all(Facility)
    
    if not all_facilities:
        abort(404)

    all_facilities = [facility.to_dict() for facility in all_facilities.values()]

    return jsonify(all_facilities)

# get all facilities from infrastructure
@app_views.route('/infrastructures/<infras_id>/facilities', methods=['GET'], strict_slashes=False)
@token_required
def get_facilities_from_infras(current_user, infras_id):
    """get all facilities from Infrastructure """
    infrastructure = storage.get(Infrastructure, infras_id)

    if not infrastructure:
        abort(400, description="Infrastructure doesn't exist")

    infras_facilities = [loc.to_dict() for loc in infrastructure.facilities]

    return jsonify(infras_facilities)

# get a facility
@app_views.route('/facilities/<facility_id>', methods=['GET'], strict_slashes=False)
@token_required
def get_facility(current_user, facility_id):
    """gets an infrastucture """
    facility = storage.get(Facility, facility_id)

    if not facility:
        abort(404)

    return jsonify(facility.to_dict())

# post a facility
@app_views.route('infrastructures/<infras_id>/facilities', methods=['POST'], strict_slashes=False)
@token_required
def post_facility(current_user, infras_id):
    """ add an facility """
    try:
        if not request.get_json():
            return {
                "status": "error",
                "data": None,
                "message": "Not a JSON"
            }, 400

        infras = storage.get(Infrastructure, infras_id)
        if not infras:
            return {
                "status": "error",
                "data": None,
                "message": "Invalid Facility ID"
            }, 404

        infras_attr = ['name', 'description']
        for val in infras_attr:
            if val not in request.get_json():
                return {
                    "status": "error",
                    "data": None,
                    "message": '{val} is missing'.format(val=val)
                }, 400

        data = request.get_json()
        instance = Facility(**data)
        instance.infrastructure_id = infras.id
        instance.save()
        
        return_data = instance.to_dict()
        return_data['infrastructure_name'] = instance.infrastructures.name
        return_data['location_name'] = instance.infrastructures.location.name

        return {
            "status": "success",
            "data": return_data,
            "message": "Record Created"
        } , 201
    
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }, 500

# put a facility
@app_views.route('/facilites/<facility_id>', methods=['PUT'], strict_slashes=False)
@token_required
def put_facility(current_user, facility_id):
    """updates an facility info"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    facility = storage.get(Infrastructure, facility_id)
    if not facility:
        return {
            "status": "error",
            "data": None,
            "message": "Invalid Facility ID"
            }

    ignore = ['id', 'updated_at', 'created_at']

    data = request.get_json()
    for key, value in facility.items():
        if key not in ignore:
            setattr(facility, key, value)
    storage.save()

    return make_response(facility.to_dict(), 200)

# delete a facility
@app_views.route('/facilities/<facility_id>', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_facility(current_user, facility_id):
    """deletes an infrastucture """
    try:
        facility = storage.get(Facility, facility_id)

        if not facility:
            return {
            "status": "error",
            "data": None,
            "message": "Invalid Facility ID"
            }

        storage.delete(facility)
        storage.save()

        return jsonify({"status": "success", "data": {}, "message": "Record Deleted"}), 200
    
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }, 500
