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
                "error": "Invalid payload"
            }
        
        job = None
        for j in jobs:
            if j.id == data.get('job_id'):
                job = j
        if not job:
            return {
                "error": "Invalid job id"
            }
        job.status = "Done"
        damage = job.damages
        damage.state = "Awaiting Verification"
        damage.save()
        job.save()
        return {
            "status": True
        }
    except Exception as e:
        return {
            "error": str(e)
         }
