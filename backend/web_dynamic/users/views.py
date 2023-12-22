#!/usr/bin/python3
"""User routes"""

from os import getcwd, mkdir, path
from flask import (
    Blueprint,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory)
import jwt
from helper_files.auth_middleware import user_token_required
from werkzeug.utils import secure_filename
from helper_files.validate import validate_email_and_password, validate_user

from models import storage
from models.damage import Damage, priority_lst
from models.damage_category import DamageCategory
from models.facility import Facility
from models.image import Image
from models.location import Location
from models.student_user import StudentUser

user_views = Blueprint(
    'user_views',
    __name__,
    url_prefix='',
    static_folder='static')


def get_user():
    """gets a user if they are logged in

    Args:

    Returns:
        None or User: None or User
    """
    token = None
    if request.cookies.get('user_access_token'):
        token = request.cookies.get('user_access_token')

    if not token:
        return None
    print(token)
    try:
        data = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"])
        print(data)
        current_user = storage.get(StudentUser, data['user_id'])

        if current_user is None:
            return None

    except Exception as e:
        return None

    return current_user


@user_views.route('/', methods=['GET'])
def user_home():
    """ user home page """
    all_damages = storage.all(Damage).values()
    return render_template(
        'users/home.html',
        all_damages=all_damages,
        home=True,
        user=get_user())


@user_views.route('/login', methods=['GET', 'POST'])
def user_login():
    """ user login route """
    if request.method == 'GET':
        return render_template('users/login.html')

    if request.method == 'POST':
        try:
            data = dict(request.form)
            if not data:
                flash('Please provide user details', category='danger')
                return render_template('users/login.html')

            # validate input
            is_validated = validate_email_and_password(
                data.get('email'), data.get('password'))
            if not is_validated:
                flash(
                    is_validated.get(
                        'message',
                        "Invalid data"),
                    category='danger')
                return render_template('users/login.html')

            user = StudentUser.login(data['email'], data['password'])

            if user:
                try:
                    token = jwt.encode(
                        {"user_id": user.id},
                        current_app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )
                    response = make_response(redirect('/'))
                    response.set_cookie('user_access_token', token)
                    return response
                except Exception as e:
                    flash('Something went wrong!', category='danger')
                    return render_template('users/login.html')

            flash(
                'Error fetching auth token!, invalid email or password',
                category='danger')
            return render_template('users/login.html')
        except Exception as e:
            flash('Something went wrong1!', category='danger')
            return render_template('users/login.html')


@user_views.route('/register', methods=['GET', 'POST'])
def user_register():
    """ user register route """
    if request.method == 'GET':
        return render_template('users/register.html')

    if request.method == 'POST':

        try:
            user = dict(request.form)
            print(request.form)

            if not user:
                flash("Please provide user details", category="danger")
                return render_template('users/register.html')

            is_validated = validate_user(**user)
            if is_validated is not True:
                flash("\n".join(is_validated.values()), category="danger")
                return render_template('users/register.html')

            email_exists = StudentUser.get_by_email(user['email'])

            if email_exists:
                flash("User email already exist", category="danger")
                return render_template('users/register.html')

            user = StudentUser(**user)

            user.save()

            return render_template('users/login.html', form="Sign In")

        except Exception as e:
            flash("Something went wrong1", category="danger")
            return render_template('users/register.html')


@user_views.route('/logout', methods=['GET'])
def user_logout():
    """logout for worker """
    response = make_response(redirect('/login'))
    response.delete_cookie('user_access_token')
    return response


@user_views.route('/report', methods=['GET', 'POST'])
@user_token_required
def report_damage(current_user):
    """ user report damage """
    categories = storage.all(DamageCategory).values()
    priorities = priority_lst
    locations = storage.all(Location).values()
    if request.method == 'GET':
        return render_template(
            'users/report_damage.html',
            categories=categories,
            priorities=priorities,
            locations=locations,
            user=current_user)

    try:
        current_path = getcwd()
        data = request.form
        files = request.files.getlist('images')

        if not data or not files:
            flash("Invalid form data", category="danger")
            return render_template(
                'users/report_damage.html',
                categories=categories,
                priorities=priorities,
                locations=locations)

        facility = storage.get(Facility, data.get('facility', None))

        if not facility and not data.get('new_facility', None):
            flash("Facility doesn't exist", category="danger")
            return render_template(
                'users/report_damage.html',
                categories=categories,
                priorities=priorities,
                locations=locations)

        new_facility = data.get('new_facility', None)
        if new_facility:
            new_facility.strip('"')
            facility = Facility(
                name=new_facility,
                description="User generated Facility to be reviewed")
            if not data.get('infras', None):
                flash("Invalid Infrastructure ID", category='danger')
                return render_template(
                    'users/report_damage.html',
                    categories=categories,
                    priorities=priorities,
                    locations=locations)

            facility.infrastructure_id = data.get('infras')
            facility.save()

        damage_attr = ['description', 'priority', 'category']
        for attr in damage_attr:
            if attr not in data.keys():
                flash(
                    "{attr} is missing.".format(
                        attr=attr),
                    category='danger')

                return render_template(
                    'users/report_damage.html',
                    categories=categories,
                    priorities=priorities,
                    locations=locations)

        category = storage.get(DamageCategory, data.get('category', None))

        if not category:
            categories = storage.all(DamageCategory).values()
            for cat in categories:
                if cat.name == "Others":
                    category = cat
                    break

        instance = Damage(**data)
        instance.facility_id = facility.id
        instance.reporter_id = current_user.id
        instance.category_id = category.id
        instance.priority = data.get('priority')
        instance.save()

        image_dir = f'{current_path}/web_dynamic/static/images/{instance.id}'
        try:
            mkdir(image_dir)
        except BaseException:
            print('already exists')

        len(files)
        for f in files:
            print(f)
        print(type(files), files)
        for f in files:
            print(f)
            filename = secure_filename(f.filename)
            image = Image(name=filename)
            image.damage_id = instance.id
            image.save()
            f.save(path.join(image_dir, filename))

        return redirect(f'/damages/{instance.id}', )
    except Exception as e:
        flash(e, category='danger')
        return render_template(
            'users/report_damage.html',
            user=current_user,
            categories=categories,
            priorities=priorities,
            locations=locations)


@user_views.route('/damages/<damage_id>', methods=['GET'])
def view_damage(damage_id):
    """ view damage info """
    damage = storage.get(Damage, damage_id)

    if not damage:
        flash("Damage was not found", category='danger')
        return render_template('users/damage.html')

    damage.category = storage.get(DamageCategory, damage.category_id)
    return render_template('users/damage.html', damage=damage, user=get_user())


@user_views.route('/reports')
@user_token_required
def user_reports(current_user):
    """returns damages reported by users
    """
    damages = storage.all(Damage).values()
    damages = [
        damage for damage in damages if damage.reporter_id == current_user.id]
    verify_damage = [damage for damage in damages if damage.state == 'Awaiting Verification']
    return render_template(
        '/users/my-reports.html',
        all_damages=damages,
        user=current_user, verify_damage=verify_damage)
