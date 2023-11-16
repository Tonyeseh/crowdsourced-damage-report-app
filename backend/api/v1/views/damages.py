#!/usr/bin/python3
""" Damages Route module """

from crypt import methods
from flask import abort, jsonify, make_response, request
from models import storage
from models.facility import Facility
from models.image import Image
from models.damage import Damage
from models.student_user import StudentUser
from models.damage_category import DamageCategory
from api.v1.views import app_views

# get all damages
@app_views.route('/damages', methods=['GET'], strict_slashes=False)
def get_damages():
    """ gets all damages """
    all_damages = storage.all(Damage)

    if not all_damages:
        abort(404)

    all_damages = [dam.to_dict() for dam in all_damages.values()]

    return jsonify(all_damages)

# get all damages in a facility
@app_views.route('/facilities/<facility_id>/damages', methods=['GET'], strict_slashes=False)
def get_facility_damage(facility_id):
    """gets all damages in a facility"""
    facility = storage.get(Facility, facility_id)

    if not facility:
        abort(404, description="Facility doesn't exist")

    damages = [dam.to_dict() for dam in facility.damages]
    return jsonify(damages)

# get a damage
@app_views.route('/damages/<damage_id>', methods=['GET'], strict_slashes=False)
def get_damage(damage_id):
    """ gets a damage """
    damage = storage.get(Damage, damage_id)

    if not damage:
        abort(404)

    return jsonify(damage.to_dict())

# post a damage
@app_views.route('/facilities/<facility_id>/damages', methods=['POST'], strict_slashes=False)
def post_damage(facility_id):
    """ posts a facility """
    if not request.get_json():
        abort(400, description="Not a JSON")

    facility = storage.get(Facility, facility_id)

    if not facility:
        abort(404, description="Facility doesn't exist")

    data = request.get_json()

    damage_attr = ['priority', 'description']
    for attr in damage_attr:
        if attr not in data.keys():
            abort(400, description="{attr} is missing.".format(attr=attr))

    instance = Damage(**data)
    instance.facility_id = facility.id
    instance.reporter_id = StudentUser(email="dummy@mail.com", password="dummy_password", first_name="dummy first_name", last_name="dummy last_name")
    instance.category_id = DamageCategory(name="electricity")

    image = Image(name="one_image")
    image.damage_id = instance

    instance.save()

    
    return make_response(jsonify(instance.to_dict()), 201)

# put a damage
@app_views.route('/damages/<damage_id>', methods=['PUT'], strict_slashes=False)
def put_damage(damage_id):
    """update damage"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    damage = storage.get(Damage, damage_id)

    if not damage:
        abort(404)

    return make_response(jsonify(damage.to_dict()), 200)

# delete a damage
@app_views.route('/damages/<damage_id>', methods=['DELETE'], strict_slashes=False)
def delete_damage(damage_id):
    """ deletes a damage """
    damage = storage.get(Damage, damage_id)

    if not damage:
        abort(404)

    storage.delete(damage)
    storage.save()

    return jsonify({}), 200

# search for damages 
