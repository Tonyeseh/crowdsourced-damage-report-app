from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from models import storage
from models.admin_user import AdminUser


def token_required(func):
    """ wrapper function for token required routes """
    @wraps(func)
    def decorated(*args, **kwargs):
        """decorated function"""
        token = None
        if "Authorization" in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unathorized",
            }, 401
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = storage.get(AdminUser, data['user_id'])

            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unathorized"
                }, 401
            if not current_user['active']:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        
        return func(current_user, *args, **kwargs)
    
    return decorated
