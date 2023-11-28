#!/usr/bin/python3
""" auth route module """

from hashlib import md5
from api.v1.views import app_views
from models import storage
from models.student_user import StudentUser

# login
from flask import abort, jsonify, request

@app_views.route('/auth/login', methods=["POST"], strict_slashes=False)
def login_auth():
    """login path for student users"""
    user = {}
    form_data = request.form.to_dict()

    email = form_data.get('email', None)
    password = form_data.get('password', None)

    if not email or not password:
        abort(400, description="Invalid Payload")

    password = md5(password.encode()).hexdigest()

    all_students = storage.all(StudentUser)

    for stud in all_students.values():
        if stud.email == email and password == stud.password:
            user = stud
            break
            

    return jsonify(user)

# signup
def sign_up_auth():
    """sign up path for student us"""
    pass

