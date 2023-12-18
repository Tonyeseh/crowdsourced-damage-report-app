#!/usr/bin/python3
""" Blueprint for API """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.locations import *
from api.v1.views.infrastructures import *
from api.v1.views.facilities import *
from api.v1.views.damages import *
from api.v1.views.categories import *
from api.v1.views.student_users import *
from api.v1.views.auth import *
from api.v1.views.categories import *
from api.v1.views.admin_user import *
from api.v1.views.worker import *
