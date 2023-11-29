#!/usr/bin/python3
""" adminUser route module """

import jwt
from flask import current_app, request
from api.v1.views import app_views
from models import storage
from models.admin_user import AdminUser
from api.v1.validate import validate_email_and_password

@app_views.route('/admin/login', methods=['POST'])
def admin_login():
    """login route for admin users"""
    try:
        data = request.json
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
        user = storage.get_by_email(AdminUser, data['email'])
        if user:
            if user.validate_password(data['password']):
                try:
                    user['token'] = jwt.encode(
                        {"user_id": user.id},
                        current_app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )
                    return {
                        "message": "Successfully fetched auth token",
                        "data": user
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
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500
