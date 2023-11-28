#!/usr/bin/python3
""" Categories Route module """

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.damage import Damage
from models.damage_category import DamageCategory

@app_views.route('/categories', methods=['GET'], strict_slashes=False)
def get_categories():
    """gets all categories"""
    damages = storage.all(Damage).values()
    all_cat = [cat.to_dict() for cat in storage.all(DamageCategory).values()]
    for dam in damages:
        for cat in all_cat:
            if cat['id'] == dam.category_id:
                cat['damage_count'] = cat.get('damage_count', 0) + 1
                break
        
    return jsonify(all_cat)


def get_category(cat_id):
    """ get a category"""
    pass

@app_views.route('/categories', methods=['POST'], strict_slashes=False)
def post_category():
    """ post category """
    categories = storage.all(DamageCategory).values()
    data = request.get_json()

    if not data or "name" not in data.keys():
        abort(400, description="Bad Request")

    for cat in categories:
        if data.get('name') == cat.name:
            return jsonify({"status": "error", "message": "category already exists"})

    cat = DamageCategory(**data)
    cat.save()
    return jsonify(cat.to_dict())

def put_category(cat_id):
    """update a category"""
    pass

@app_views.route('/categories/<cat_id>', methods=["DELETE"], strict_slashes=False)
def delete_category(cat_id):
    """ delete a category """
    cat = storage.get(DamageCategory, cat_id)

    if not cat:
        abort(404)
    storage.delete(cat)
    storage.save()

    return jsonify({})
