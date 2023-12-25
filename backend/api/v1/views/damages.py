#!/usr/bin/python3
""" Damages Route module """

from os import getcwd, mkdir, path
from flask import abort, jsonify, make_response, request
from models.location import Location
from models import storage
from models.facility import Facility
from models.image import Image
from models.damage import Damage
from models.student_user import StudentUser
from models.damage_category import DamageCategory
from api.v1.auth_middleware import token_required, user_token_required
from api.v1.views import app_views
from werkzeug.utils import secure_filename

from models.worker import Worker
from models.working_on import WorkingOn

# helper functions
def add_damage_info(damage: Damage):
    """adds some information to the damage object"""

    damage.facility_name =  damage.facilities.name
    damage.infrastructure_name = damage.facilities.infrastructures.name
    damage.location_name = damage.facilities.infrastructures.location.name
    damage.img_url = [f'/images/{damage.id}/{img.name}' for img in damage.images]
    reporter =  storage.get(StudentUser, damage.reporter_id)
    damage.reporter = reporter.first_name
    
    workers = storage.all(Worker).values()
    
    damage.workers = [worker.to_dict() for worker in workers if worker.job_type == damage.category_id]

    damage = damage.to_dict()

    return remove_irrelevant_info(damage)

def remove_irrelevant_info(damage):
    try:
        del damage['facilities']
        del damage['images']
        
    except Exception as e:
        pass

# get all damages
@app_views.route('/damages', methods=['GET'], strict_slashes=False)
def get_damages():
    """ gets all damages """
    all_damages = storage.all(Damage)

    if not all_damages:
        abort(404)

    all_damages_lst = []

    for dam in all_damages.values():
        all_damages_lst.append(add_damage_info(dam))

    return jsonify(all_damages_lst)

# get all damages in a facility
@app_views.route('/facilities/<facility_id>/damages', methods=['GET'], strict_slashes=False)
def get_facility_damage(facility_id):
    """gets all damages in a facility"""
    facility = storage.get(Facility, facility_id)

    if not facility:
        abort(404, description="Facility doesn't exist")

    damages = facility.damages

    damages_lst = []
    for dam in damages:
        damages_lst.append(add_damage_info(dam))

    return jsonify(damages_lst)

# get a damage
@app_views.route('/damages/<damage_id>', methods=['GET'], strict_slashes=False)
def get_damage(damage_id):
    """ gets a damage """
    damage = storage.get(Damage, damage_id)

    if not damage:
        abort(404)

    return jsonify(add_damage_info(damage))

# post a damage
@app_views.route('/facilities/<facility_id>/damages', methods=['POST'], strict_slashes=False)
@user_token_required
def post_damage(current_user, facility_id):
    """ posts a facility """
    supported_types = ['jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'gif', 'apng', 'png', 'avif', 'svg', 'webp', 'mp4', 'ogg', 'WebM']
    current_path = getcwd()

    formData = request.form.to_dict()
    files = request.files.to_dict()

    if not formData or not files:
        abort(400, description="Invalid Payload")

    facility = storage.get(Facility, facility_id)

    if not facility and not formData.get('otherNames', None):
        abort(404, description="Facility doesn't exist")

    new_facility = formData.get('otherNames', None)
    if new_facility:
        new_facility.strip('"')
        facility = Facility(name=new_facility, description="User generated Facility to be reviewed")
        if not formData.get('infras_name', None):
            abort(404, description="Invalid Infrastructure ID")
        facility.infrastructure_id = formData.get('infras_name')
        facility.save()

    damage_attr = ['description', "category_id"]
    for attr in damage_attr:
        if attr not in formData.keys():
            abort(400, description="{attr} is missing.".format(attr=attr))

    print(formData)

    category = storage.get(DamageCategory, formData.get('category_id', None))

    if not category:
        categories = storage.all(DamageCategory).values()
        for cat in categories:
            if cat.name == "Others":
                category = cat
                break


    instance = Damage(**formData)
    instance.facility_id = facility.id
    instance.reporter_id = current_user.id
    instance.category_id = category.id
    instance.save()

    image_dir = f'{current_path}/images/{instance.id}'
    try:
        mkdir(image_dir)
    except:
        print('already exists')


    for file in files.values():
        filename = secure_filename(file.filename)
        image = Image(name=filename)
        image.damage_id = instance.id
        image.save()
        file.save(path.join(image_dir, filename))

    return make_response(jsonify(add_damage_info(instance)), 201)

# put a damage
@app_views.route('/damages/<damage_id>', methods=['PUT'], strict_slashes=False)
@token_required
def put_damage(current_user, damage_id):
    """update damage"""
    try:
        damage = storage.get(Damage, damage_id)

        if not damage:
            return {
                "status": "error", 
                "data": None,
                "message": "Invalid Damage ID"
            }, 404

        ignore = ['id', 'updated_at', 'created_at', 'worker_id']
    
        data = dict(request.form)

        for key, value in data.items():
            if key not in ignore:
                setattr(damage, key, value)
                
        if data.get('worker_id', None):
            worker = storage.get(Worker, data.get('worker_id'))
            if not worker:
                return {
                    "status": "error", 
                    "data": None,
                    "message": "Invalid Category ID"
                }, 404

            if damage.working_on and sorted(damage.working_on, key=lambda x: x.created_at, reverse=True)[0].status != 'Failed':
                return {
                    "status": "error", 
                    "data": None,
                    "message": "Damage is already Assigned"
                }
                    
            
            repair = WorkingOn()
            repair.damage_id = damage.id
            repair.worker_id = worker.id
            damage.state = "Assigned"
            damage.save()
            repair.save()
            
        return_data = {
            "worker_name": " ".join([repair.workers.first_name, repair.workers.last_name]),
            "damage_state": damage.state,
        }
                
        return jsonify({"status": "success", "data":return_data, "message": "Record Updated Successfully"})
        
    except Exception as e:
        return {
            "message": str(e),
            "data": None,
            "status": "error"
        }


    # return make_response(jsonify(add_damage_info(damage)), 200)

# delete a damage
@app_views.route('/damages/<damage_id>', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_damage(current_user, damage_id):
    """ deletes a damage """
    damage = storage.get(Damage, damage_id)

    if not damage:
        return {
            "status": "error", 
            "data": None,
            "message": "Invalid Damage ID"
        }

    storage.delete(damage)
    storage.save()

    return jsonify({
        "status": "success",
        "data": {},
        "message": "Record Deleted"
    }), 200

#get workers for a damage
@app_views.route('/damages/<damage_id>/workers', methods=['GET'])
@token_required
def damage_worker(current_user, damage_id):
    """gets the workers that can work on a damage"""
    damage = storage.get(Damage, damage_id)
    
    if not damage:
        abort(404)
    
    category = storage.get(DamageCategory, damage.category_id)
    
    if not category:
        abort(404)
        
    workers = [cat.to_dict() for cat in category.workers]
    
    return jsonify(workers), 200


# get damages reported by a particular User
@app_views.route('/users/damages')
@user_token_required
def get_report_by_user(current_user):
    """ gets report by User """

    user_report = [add_damage_info(report) for report in current_user.reports]
    print(user_report)
    return jsonify(user_report)

@app_views.route('/damages/info', methods=["GET"], strict_slashes=False)
@token_required
def damage_info(current_user):
    """ gets total info of the damages """
    damages = storage.all(Damage)
    
    completed_damage = [dam for dam in damages.values() if dam.state == "Completed"]
    assigned_damage = [dam for dam in damages.values() if dam.state == "Assigned"]
    in_review_damage = [dam for dam in damages.values() if dam.state == "Awaiting Verification"]

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


    return jsonify({"completed": len(completed_damage),
                    "assigned": len(assigned_damage),
                    "in_review": len(in_review_damage),
                    "all": len(damages),
                    "locations": locations})

# search for damages 


@app_views.route('/damages/working_on', methods=['POST'])
@token_required
def post_working_on(current_user):
    """ creates a new working_on entry"""
    all_works = storage.all(WorkingOn)
    work = None
    try:
        data = request.form
        if ['damage_id', 'worker_id'] != list(data.keys()):
            return {
                "error": "Incomplete data"
            }
            
        damage = storage.get(Damage, data['damage_id'])
        worker = storage.get(Worker, data['worker_id'])
        if not damage or not worker:
            return {
                "error": "Invalid damage or worker id"
            }
        
        for works in all_works.values():
            if works.damage_id == damage.id and works.status == "In Progress":
                work = works
                
        if work:
            work.worker_id = worker.id
            damage.state = "Assigned"
            damage.save()
            
        else:
            work = WorkingOn()
            work.damage_id = damage.id
            work.worker_id = worker.id
            damage.state = "Assigned"
            damage.save()

        work.save()
        return {
            "status": True
        }
        
    except Exception as e:
        return {"error": str(e)}
