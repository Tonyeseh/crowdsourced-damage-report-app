#!/usr/bin/python3
""" Categories Route module """

from flask import jsonify, request
from api.v1.auth_middleware import admin_token_required
from api.v1.views import app_views
from models import storage
from models.damage import Damage
from models.damage_category import DamageCategory

@app_views.route('/categories', methods=['GET'], strict_slashes=False)
@admin_token_required
def get_categories(current_user):
    """gets all categories"""
    try:
        damages = storage.all(Damage).values()
        all_cat = [cat.to_dict() for cat in storage.all(DamageCategory).values()]
        for dam in damages:
            for cat in all_cat:
                if cat['id'] == dam.category_id:
                    cat['damage_count'] = cat.get('damage_count', 0) + 1
                    break
            
        return jsonify(all_cat)
    
    except Exception as e:
        return {
            "message": str(e),
            "data": None,
            "status": "error"
        }, 500

@app_views.route('/categories/<cat_id>')
@admin_token_required
def get_category(current_user, cat_id):
    """ get a category"""
    try:
        cat = storage.get(DamageCategory, cat_id)
        
        if not cat:
            return {
                "status": "error",
                "data": None,
                "message": "Invalid Category ID"
            }, 404
            
        return {
            "status": "success",
            "data": cat.to_dict(),
            "message": "data returned"
        }
        
    except Exception as e:
        return {
            "message": str(e),
            "data": None,
            "status": "error"
        }, 500

@app_views.route('/categories', methods=['POST'], strict_slashes=False)
@admin_token_required
def post_category(current_user):
    """ post category """
    try:
        categories = storage.all(DamageCategory).values()
        data = request.get_json()

        if not data or "name" not in data.keys():
            return {
                "status": "error",
                "data": None,
                "message": "Invalid payload"
            }, 400

        for cat in categories:
            if data.get('name') == cat.name:
                return jsonify({"status": "error", "data": None, "message": "category already exists"}), 400

        cat = DamageCategory(**data)
        cat.save()
        return jsonify({"status": "success", "data": cat.to_dict(), "message": "Category Added"}), 201
    
    except Exception as e:
        return {
            "message": str(e),
            "data": None,
            "status": "error"
        }, 500

@app_views.route('/categories/<cat_id>', methods=['PUT'])
@admin_token_required
def put_category(current_user, cat_id):
    """update a category"""
    try:
        cat = storage.get(DamageCategory, cat_id)
        
        data = request.form
        
        if not data or "name" not in data.keys():
            return {
                "status": "error",
                "data": None,
                "message": "Invalid payload"
            }, 400
            
        ignore = ['id', 'created_at', 'updated_at']
            
        if not cat:
            return {
                "status": "error",
                "data": None,
                "message": "Invalid Category ID"
            }, 404
        
        for key, value in data.items():
            if key not in ignore:
                setattr(cat, key, value)
                
        cat.save()
                
        return {
            "status": "success",
            "data": cat.to_dict(),
            "message": "Record Updated"
        }
        
    except Exception as e:
        return {
            "message": str(e),
            "data": None,
            "status": "error"
        }, 500

@app_views.route('/categories/<cat_id>', methods=["DELETE"], strict_slashes=False)
@admin_token_required
def delete_category(current_user, cat_id):
    """ delete a category """
    try:
        cat = storage.get(DamageCategory, cat_id)

        if not cat:
            return {
                "status": "error", 
                "data": None,
                "message": "Invalid Category ID"
            }, 404
        storage.delete(cat)
        storage.save()

        return jsonify({
            "status": "success",
            "data": {},
            "message": "Record Deleted"
        })
    except Exception as e:
        return {
            "message": str(e),
            "data": None,
            "status": "error"
        }, 500
