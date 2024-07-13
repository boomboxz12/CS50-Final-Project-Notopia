import sqlite3

from flask import flash, Flask, redirect, render_template, request, session, url_for
from flask_session import Session

from helpers import login_required

# Configuring Flask, the session, and the response
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "cachelib"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Preparing the sqlite3 databases for use
users_con = sqlite3.connect("users.db")
users_cur = users_con.cursor()
try:
    current_user_name = users_cur.execute("""
                                          SELECT *
                                          FROM users
                                          WHERE user_id = ?
                                          """,
                                          session["user_id"])
    notes_con = sqlite3.connect(f"{current_user_name}.db")
    notes_cur = notes_con.cursor()
except:
    pass


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return render_template("logout.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


# Close any open databases
users_con.close()
try:
    notes_con.close()
except:
    pass
