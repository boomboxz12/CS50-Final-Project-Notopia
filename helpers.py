import sqlite3

from flask import redirect, render_template, session, url_for
from functools import wraps


# Function that prevents access to protected pages/routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user_id"] == None:
            return redirect(url_for("/login"))
        return f(*args, **kwargs)
    

# Interaction with sqlite3 database
def sql(database, query, *qmarks):
    with sqlite3.connect(database) as con:
        cur = con.cursor()
        result = cur.execute(query, *qmarks)
        return result
    
def apologize(source, message="An unknown error has occurred. Please try again later. We apologize for the inconvenience.", code=400):
    return render_template("error.html", source=source, message=message, code=code), code