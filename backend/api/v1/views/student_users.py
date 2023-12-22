#!/usr/bin/python3
""" student_users route module """

import jwt

from flask import current_app, abort, jsonify, request
from api.v1.views import app_views
from api.v1.auth_middleware import user_token_required
from api.v1.validate import validate_user, validate_email_and_password
from models import storage
from models.damage import Damage
from models.student_user import StudentUser

# get all student_users


@app_views.route('/users/', methods=["GET"], strict_slashes=False)
@user_token_required
def get_student_user(current_user):
    """ get a student """
    # user = storage.get(StudentUser, user_id)

    # if not user:
    #     abort(404)

    return jsonify(current_user.to_dict())

# post student_users


@app_views.route('/users', methods=["POST"])
def post_user():
    """ signup as a user """
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
        email_exists = StudentUser.get_by_email(user['email'])

        if email_exists:
            return {
                "message": "User email already exist",
                "data": None,
                "error": "Invalid email address"
            }
        user = StudentUser(**user)
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

# login user
@app_views.route('/users/login', methods=['POST'])
def login_user():
    """login user to the platform"""
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
        user = StudentUser.login(data['email'], data['password'])
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



# put student_users
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def put_student_user(user_id):
    """ get a student """
    user = storage.get(StudentUser, user_id)

    if not user:
        abort(404)

    
    ignore = ['id', 'updated_at', 'created_at']
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)

    return jsonify(user.to_dict())


@app_views.route('/users/verify', methods=['POST'], strict_slashes=False)
@user_token_required
def verify_damage(current_user):
    """ verify a damage """
    try:
        data = dict(request.form)
        print(data)

        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400

        if 'damage_id' not in data.keys() and 'verify' not in data.key():
            return {
                "message": "Invalid payload",
                "data": None,
                "error": "Bad request",
            }, 400
            
        damage = storage.get(Damage, data.get('damage_id'))
        if not damage:
            return {
                "message": "Invalid damage instance",
                "data": None,
                "error": "Bad request"
            }, 400
            
        job = None
        for j in damage.working_on:
            if job is None:
                job = j
                continue
            if j.created_at > job.created_at:
                job = j
        
        if not job:
            return {
                "message": "Damage is not yet being worked on",
                "data": None,
                "error": "Bad request"
            }, 400
            
        if data.get('verify') == 'Yes':
            job.status = "Done"
            damage.state = "Completed"
            job.save()
            damage.save()
            
        else:
            job.status = "Failed"
            damage.state = "Failed"
            job.save()
            damage.save()
            

        return {
            "data": "Updated"
        }

    except Exception as e:
        return {
            "message": "Something went wrong1!",
            "error": str(e),
            "data": None
        }, 500
