#!/usr/bin/python3
""" student_users route module """

from flask import request
from api.v1.auth_middleware import worker_token_required
from api.v1.views import app_views

@app_views.route('/worker/damages/working_on', methods=['POST'])
@worker_token_required
def update_job_status(current_user):
    """ update job status """
    jobs = current_user.jobs
    
    try:
        data = request.form
        
        if not data.get('job_id', None) or not data.get('status', None):
            return {
                "status": "error",
                "data": None,
                "message": "Invalid payload"
            }, 400
        
        job = None
        for j in jobs:
            if j.id == data.get('job_id'):
                job = j
        if not job:
            return {
                "status": "error",
                "data": None,
                "message": "Invalid Job ID"
            }, 404
        if job.status == "Done":
            return {
                "status": "error",
                "data": None,
                "message": "Already marked as done"
            }, 400
        job.status = "Done"
        damage = job.damages
        damage.state = "Awaiting Verification"
        damage.save()
        job.save()
        
        return_data = job.to_dict()
        try:
            del return_data['damages']
        except:
            pass
        
        return {
            "status": "success",
            "data": return_data,
            "message": "Job marked as Done"
        }, 200
    except Exception as e:
        return {
                "status": "error",
                "data": None,
                "message": str(e)
            }, 500
