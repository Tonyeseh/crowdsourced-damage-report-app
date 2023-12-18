#!/usr/bin/python3
"""Admin routes"""

from flask import (
    Blueprint,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request)
import jwt
from api.v1.views.damages import add_damage_info

from helper_files.auth_middleware import token_required
from helper_files.validate import validate_email_and_password, validate_user
from models import storage
from models.admin_user import AdminUser
from models.damage import Damage
from models.damage_category import DamageCategory
from models.facility import Facility
from models.infrastructure import Infrastructure
from models.location import Location


admin_views = Blueprint(
    'admin_views',
    __name__,
    url_prefix='/admin',
    static_folder='static')


@admin_views.route('/', methods=['GET'])
@token_required
def admin_home(current_user):
    """admin's home page """
    damages = storage.all(Damage)

    completed_damage = [
        dam for dam in damages.values() if dam.state == "Completed"]
    assigned_damage = [
        dam for dam in damages.values() if dam.state == "Assigned"]
    in_review_damage = [dam for dam in damages.values(
    ) if dam.state == "Awaiting Verification"]

    # location info
    locations = [loc.to_dict() for loc in storage.all(Location).values()]

    for dam in damages.values():
        loc_id = dam.facilities.infrastructures.location.id
        for loc in locations:
            if loc['id'] == loc_id:
                loc['damage_count'] = loc.get("damage_count", 0) + 1
                if dam.state == "completed":
                    loc['completed'] = loc.get('completed', 0) + 1
                for work in dam.working_on:
                    if dam.state == "completed":
                        loc['cost'] = loc.get('cost', 0) + work.actual_cost
                    else:
                        loc['cost'] = loc.get('cost', 0) + work.proposed_cost

    return render_template(
        'admin/dashboard.html',
        user=current_user,
        page='dashboard',
        damage_info={
            "completed": len(completed_damage),
            "assigned": len(assigned_damage),
            "in_review": len(in_review_damage),
            "all": len(damages),
            "locations": locations})


@admin_views.route('/login', methods=['GET', 'POST'])
def admin_login():
    """login for admin"""
    form = "Sign In"
    if request.method == 'GET':
        return render_template('admin/login.html', form=form)

    if request.method == 'POST':
        try:
            data = dict(request.form)
            print(data)
            if not data:
                flash("Please provide your details", category="danger")
                return render_template('admin/login.html', form=form)

            # validate input
            is_validated = validate_email_and_password(
                data.get('email'), data.get('password'))
            print(is_validated)

            if is_validated is not True:
                print('\n'.join(is_validated.values()))
                flash('\n'.join(is_validated.values()), category="danger")
                return render_template('admin/login.html', form=form)
            user = AdminUser.login(data['email'], data['password'])
            print(user)
            user1 = AdminUser.get_by_email(data['email'])
            print(user1)
            if user:
                try:
                    token = jwt.encode(
                        {"user_id": user.id},
                        current_app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )

                    response = make_response(redirect('/admin/'))
                    response.set_cookie('admin_access_token', token)
                    return response
                except Exception as e:
                    flash("Something went wrong!", category="danger")
                    return render_template('admin/login.html', form=form)
            flash(
                "Error fetching auth token!, invalid email or password",
                category="danger")
            return render_template('admin/login.html', form=form)
        except Exception as e:
            flash("Something went wrong!", category="danger")
            return render_template('admin/login.html', form=form)


@admin_views.route('/logout', methods=['GET'])
def admin_logout():
    """logout for admin """
    response = make_response(redirect('/admin/login'))
    response.delete_cookie('access_token')
    return response


@admin_views.route('/register', methods=['GET', 'POST'])
def admin_register():
    """register for admin """
    form = "Sign Up"

    if request.method == 'GET':
        return render_template('admin/register.html', form=form,)

    if request.method == 'POST':
        try:
            user = dict(request.form)

            if not user:
                flash("Please provide user details", category="danger")
                return render_template('admin/register.html', form=form,)

            is_validated = validate_user(**user)
            if is_validated is not True:
                flash("\n".join(is_validated.values()), category="danger")
                return render_template('admin/register.html', form=form,)

            email_exists = AdminUser.get_by_email(user['email'])

            if email_exists:
                flash("User email already exist", category="danger")
                return render_template('admin/register.html', form=form,)

            user = AdminUser(**user)

            user.save()

            return render_template('admin/login.html', form="Sign In")

        except Exception as e:
            print(e)
            flash("Something went wrong1", category="danger")
            return render_template('admin/register.html', form=form,)


@admin_views.route('/locations', methods=['GET'])
@token_required
def get_all_locations(current_user):
    """ get all locations """
    all_locations = storage.all(Location)
    all_locations = [location for location in all_locations.values()]
    return render_template(
        'admin/location.html',
        all_locations=all_locations,
        user=current_user,
        page='location')


@admin_views.route('/infrastructures', methods=['GET'], strict_slashes=False)
@token_required
def get_infrastructures(current_user):
    """ gets all infrastructures """
    all_infras = storage.all(Infrastructure)
    locations = storage.all(Location).values()

    all_infras = [infras for infras in all_infras.values()]

    return render_template(
        'admin/infrastructure.html',
        all_infras=all_infras,
        page='infras',
        user=current_user,
        locations=locations)


@admin_views.route('/facilities', methods=['GET'])
@token_required
def get_facilities(current_user):
    """ gets all facilities """
    all_facilities = storage.all(Facility)
    locations = storage.all(Location).values()

    all_facilities = [facility for facility in all_facilities.values()]

    return render_template(
        'admin/facility.html',
        all_facilities=all_facilities,
        user=current_user,
        page='facility',
        locations=locations)


@admin_views.route('/damages', methods=['GET'])
@token_required
def get_damages(current_user):
    """ gets all damages """
    all_damages = storage.all(Damage)

    all_damages_lst = []

    for dam in all_damages.values():
        all_damages_lst.append(add_damage_info(dam))
        print(dam.workers)

    return render_template(
        'admin/damage.html',
        all_damages=all_damages_lst,
        user=current_user,
        page='damage',
    )


@admin_views.route('/categories', methods=['GET'])
@token_required
def get_categories(current_user):
    """ get all categories """
    damages = storage.all(Damage).values()
    all_cat = [cat.to_dict() for cat in storage.all(DamageCategory).values()]
    for dam in damages:
        for cat in all_cat:
            if cat['id'] == dam.category_id:
                cat['damage_count'] = cat.get('damage_count', 0) + 1
                break

    return render_template(
        'admin/category.html',
        categories=all_cat,
        user=current_user,
        page='category')
