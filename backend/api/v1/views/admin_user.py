#!/usr/bin/python3
""" adminUser route module """

import jwt
from flask import current_app, jsonify, request
from api.v1.views import app_views
from models.admin_user import AdminUser
from api.v1.validate import validate_email_and_password, validate_user

@app_views.route('/admin', methods=['POST'])
def add_admin():
    """ signup as an admin """
    try:
        user = dict(request.form)

        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user(**user)
        if is_validated is not True:
            return dict(message="Invalid data", data=None, error=is_validated)
        email_exists = AdminUser.get_by_email(user['email'])

        if email_exists:
            return {
                "message": "User email already exist",
                "data": None,
                "error": "Invalid email address"
            }
        user = AdminUser(**user)
        user.save()
        
        return jsonify({
            "message": "Successfully created new user",
            "data": user.to_dict(),
        }), 201

    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500


@app_views.route('/admin/login', methods=['POST'])
def admin_login():
    """login route for admin users"""
    try:
        data = dict(request.form)
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        
        # validate input
        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if not is_validated:
            return dict(message="Invalid data", data=None, error="is_validated"), 400
        user = AdminUser.login(data['email'], data['password'])
        print(user)
        if user:
            try:
                user.token = jwt.encode(
                    {"user_id": user.id},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user.to_dict()
                }
            except Exception as e:
                return {
                    "message": "Something went wrong!",
                    "error": str(e),
                    "data": None
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong1!",
                "error": str(e),
                "data": None
        }, 500
