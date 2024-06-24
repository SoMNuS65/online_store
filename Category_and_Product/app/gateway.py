from functools import wraps
from flask import request
from app.api.helper import send_error, send_result
import requests

def authorization_require():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            authorization = request.headers.get('Authorization', '').strip()
            try:
                res = requests.get("http://localhost:5012/api/v1/auth/token/validate", headers={"Authorization": authorization}).json()
            except Exception as ex:
                return send_error(message="You don't have permission")
            if 'message' in res and res['message']['status'] == 'success':
                return fn(*args, **kwargs)
            else:
                return send_error(message="You don't have permission")
        return decorator
    return wrapper
