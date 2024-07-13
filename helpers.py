from flask import redirect, session, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user_id"] == None:
            return redirect(url_for("/login"))
        return f(*args, **kwargs)