#!/usr/bin/python3
""" student_users route module """

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.student_user import StudentUser

# get all student_users
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def get_student_user(user_id):
    """ get a student """
    user = storage.get(StudentUser, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())

# post student_users
@app_views.route('/users', methods=["POST"], strict_slashes=False)
def post_student_user():
    """ post a student """
    data = dict(request.form)

    student_attr = ["first_name", "last_name", "email", "password"]
    for attr in student_attr:
        if attr not in data.keys():
            abort(400, description=f'{attr} is missing')

    instance = StudentUser(**data)
    instance.save()

    return jsonify(instance.to_dict()), 201

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
