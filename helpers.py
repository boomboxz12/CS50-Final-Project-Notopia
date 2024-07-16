import sqlite3

from flask import redirect, render_template, session, url_for
from functools import wraps


# Function that prevents access to protected pages/routes
def login_required(f):
    """Limit access to protected pages"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user_id"] == None:
            return redirect(url_for("/login"))
        return f(*args, **kwargs)
    

# Interaction with sqlite3 database
def sql(database: str, query: str, *qmarks: tuple):
    """Execute SQL queries (sqlite3)"""
    with sqlite3.connect(database) as con:
        cur = con.cursor()
        result = cur.execute(query, *qmarks)
        print("\n" + " ".join(query.split()) + str(qmarks) + "\n")
        return result
    
def apologize(source: str, message="An unknown error has occurred. Please try again later. We apologize for the inconvenience.", code=400):
    """Return an error"""
    return render_template("error.html", source=source, message=message, code=code), code