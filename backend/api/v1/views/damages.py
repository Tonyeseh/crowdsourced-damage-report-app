#!/usr/bin/python3
""" Damages Route module """

from crypt import methods
from os import getcwd, mkdir, path
from tarfile import SUPPORTED_TYPES
from typing import Dict, List
from flask import abort, jsonify, make_response, request
from models import storage
from models.facility import Facility
from models.image import Image
from models.damage import Damage
from models.student_user import StudentUser
from models.damage_category import DamageCategory
from api.v1.views import app_views
from werkzeug.utils import secure_filename

# helper functions
def add_damage_info(damage: Damage):
    """adds some information to the damage object"""

    damage.facility_name =  damage.facilities.name
    damage.infrastructure_name = damage.facilities.infrastructures.name
    damage.img_url = [f'/images/{damage.id}/{img.name}' for img in damage.images]

    damage = damage.to_dict()

    remove_irrelevant_info(damage)
    return damage

def remove_irrelevant_info(damage):
    del damage['facilities']
    del damage['images']

# get all damages
@app_views.route('/damages', methods=['GET'], strict_slashes=False)
def get_damages():
    """ gets all damages """
    all_damages = storage.all(Damage)

    if not all_damages:
        abort(404)

    all_damages_lst = []

    for dam in all_damages.values():
        all_damages_lst.append(add_damage_info(dam))

    return jsonify(all_damages_lst)

# get all damages in a facility
@app_views.route('/facilities/<facility_id>/damages', methods=['GET'], strict_slashes=False)
def get_facility_damage(facility_id):
    """gets all damages in a facility"""
    facility = storage.get(Facility, facility_id)

    if not facility:
        abort(404, description="Facility doesn't exist")

    damages = facility.damages

    damages_lst = []
    for dam in damages:
        damages_lst.append(add_damage_info(dam))

    return jsonify(damages_lst)

# get a damage
@app_views.route('/damages/<damage_id>', methods=['GET'], strict_slashes=False)
def get_damage(damage_id):
    """ gets a damage """
    damage = storage.get(Damage, damage_id)

    if not damage:
        abort(404)

    return jsonify(add_damage_info(damage))

# post a damage
@app_views.route('/facilities/<facility_id>/damages', methods=['POST'], strict_slashes=False)
def post_damage(facility_id):
    """ posts a facility """
    supported_types = ['jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'gif', 'apng', 'png', 'avif', 'svg', 'webp', 'mp4', 'ogg', 'WebM']
    current_path = getcwd()

    formData = request.form.to_dict()
    files = request.files.to_dict()

    if not formData or not files:
        abort(400, description="Invalid Payload")

    facility = storage.get(Facility, facility_id)

    if not facility and not formData.get('otherNames', None):
        abort(404, description="Facility doesn't exist")

    new_facility = formData.get('otherNames', None).strip('"')
    if new_facility:
        facility = Facility(name=new_facility, description="User generated Facility to be reviewed")
        if not formData.get('infras_name', None):
            abort(404, description="Invalid Infrastructure ID")
        facility.infrastructure_id = formData.get('infras_name')
        facility.save()

    damage_attr = ['description']
    for attr in damage_attr:
        if attr not in formData.keys():
            abort(400, description="{attr} is missing.".format(attr=attr))

    category = storage.all()[list(storage.all(DamageCategory).keys())[0]]
    student = storage.all()[list(storage.all(StudentUser).keys())[0]]

    instance = Damage(**formData)
    instance.facility_id = facility.id
    instance.reporter_id = student.id
    instance.category_id = category.id
    instance.save()

    image_dir = f'{current_path}/images/{instance.id}'
    try:
        mkdir(image_dir)
    except:
        print('already exists')


    for file in files.values():
        filename = secure_filename(file.filename)
        image = Image(name=filename)
        image.damage_id = instance.id
        image.save()
        file.save(path.join(image_dir, filename))

    return make_response(jsonify(add_damage_info(instance)), 201)

# put a damage
@app_views.route('/damages/<damage_id>', methods=['PUT'], strict_slashes=False)
def put_damage(damage_id):
    """update damage"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    damage = storage.get(Damage, damage_id)

    if not damage:
        abort(404)


    ignore = ['id', 'updated_at', 'created_at']
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(damage, key, value)


    return make_response(jsonify(add_damage_info(damage)), 200)

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


# get damages reported by a particular User
@app_views.route('/users/<user_id>/damages')
def get_report_by_user(user_id):
    """ gets report by User """
    user = storage.get(StudentUser, user_id)

    if not user:
        abort(404)
        
    user_report = [report.to_dict() for report in user.damages]
    return jsonify(user_report)

# search for damages 
