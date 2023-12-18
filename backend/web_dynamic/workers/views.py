#!/usr/bin/python3
"""Workers routes"""

from flask import Blueprint, current_app, flash, make_response, redirect, render_template, request
import jwt

from models import storage
from helper_files.auth_middleware import worker_token_required
from helper_files.validate import validate_email_and_password, validate_user
from models.damage import Damage
from models.damage_category import DamageCategory
from models.worker import Worker
from models.working_on import WorkingOn

worker_views = Blueprint('worker_views', __name__, url_prefix='/workers', static_folder='static')

@worker_views.route('/', methods=['GET'])
@worker_token_required
def worker_home_page(current_user):
    """ workers homepage route """

    all_jobs = {}
    outstanding_jobs = []

    for job in current_user.jobs:
        damage = storage.get(Damage, job.damage_id)
        if damage.state == 'Completed':
            all_jobs['verified'] = all_jobs.get('verified', 0) + 1

        elif damage.state == "Awaiting Verification":
            all_jobs['not_verified'] = all_jobs.get('not_verified', 0) + 1

        elif job.status == "In Progress":
            all_jobs["not_done"] = all_jobs.get('not_done', 0) + 1
            
        print(job.damages.facilities.infrastructures)
        
        outstanding_jobs = [job for job in current_user.jobs if job.status == "In Progress"]

    all_jobs['all'] = len(current_user.jobs)


    return render_template('workers/dashboard.html', user=current_user, all_jobs=all_jobs, user_jobs=outstanding_jobs)


# get worker's jobs
@worker_views.route('/jobs', methods=['GET'])
@worker_token_required
def get_all_jobs(current_user):
    """ get all workers job """
    working_on = storage.all(WorkingOn)
    
    damages = [job for job in working_on.values() if job.worker_id == current_user.id]


@worker_views.route('/login', methods=['GET', 'POST'])
def worker_login():
    """login for worker"""
    form = "Sign In"
    if request.method == 'GET':
        return render_template('workers/login.html', form=form)
    
    if request.method == 'POST':
        try:
            data = dict(request.form)
            if not data:
                flash("Please provide user details", category="danger")
                return render_template('workers/login.html',form=form)
        
            # validate input
            is_validated = validate_email_and_password(data.get('email'), data.get('password'))
            print(is_validated)

            if is_validated is not True:
                print('\n'.join(is_validated.values()))
                flash('\n'.join(is_validated.values()), category="danger")
                return render_template('workers/login.html', form=form)
            user = Worker.login(data['email'], data['password'])
            print(user)
            if user:
                try:
                    token = jwt.encode(
                        {"user_id": user.id},
                        current_app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )

                    response = make_response(redirect('/workers/'))
                    response.set_cookie('worker_access_token', token)
                    return response
                except Exception as e:
                    flash("Something went wrong!", category="danger")
                    return render_template('workers/login.html', form=form)
            flash("Error fetching auth token!, invalid email or password", category="danger")
            return render_template('workers/login.html', form=form)
        except Exception as e:
            flash("Something went wrong!", category="danger")
            return render_template('workers/login.html', form=form)

@worker_views.route('/logout', methods=['GET'])
def worker_logout():
    """logout for worker """
    response = make_response(redirect('/workers/login'))
    response.delete_cookie('worker_access_token')
    return response

@worker_views.route('/register', methods=['GET', 'POST'])
def worker_register():
    """register for worker """
    form="Sign Up"
    categories = storage.all(DamageCategory).values()

    if request.method == 'GET':
        return render_template('workers/register.html', form=form, categories=categories)
    
    if request.method == 'POST':
        print(categories)
        try:
            user = dict(request.form)

            if not user:
                flash("Please provide user details", category="danger")
                return render_template('workers/register.html', form=form, categories=categories)
            
            is_validated = validate_user(**user)
            if is_validated is not True:
                flash("\n".join(is_validated.values()), category="danger")
                return render_template('workers/register.html', form=form, categories=categories)
            
            email_exists = Worker.get_by_email(user['email'])

            if email_exists:
                flash("User email already exist", category="danger")
                return render_template('workers/register.html', form=form, categories=categories)
            
            category_id = user.get('category', None)
            category = storage.get(DamageCategory,  category_id)
            
            user = Worker(**user)
            if not category:
                flash("Pick a valid job category", category="danger")
                return render_template('workers/register.html', form=form, categories=categories)

            user.job_type = category.id
            
            user.save()
            

            return render_template('workers/login.html', form="Sign In")

        except Exception as e:
            print(e)
            flash("Something went wrong1", category="danger")
            return render_template('workers/register.html', form=form, categories=categories)
