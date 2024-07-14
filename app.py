import sqlite3

from flask import flash, Flask, redirect, render_template, request, session, url_for
from flask_session import Session

from helpers import *

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

# # Preparing the sqlite3 databases for use
# users_con = sqlite3.connect("users.db")
# users_cur = users_con.cursor()
# try:
#     current_user_name = users_cur.execute("""
#                                           SELECT *
#                                           FROM users
#                                           WHERE user_id = ?
#                                           """,
#                                           session["user_id"])
#     notes_con = sqlite3.connect(f"{current_user_name}.db")
#     notes_cur = notes_con.cursor()
# except:
#     pass


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
    # User reached route via POST
    if request.method == "POST":
        # Receive the user's information
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the username is valid
        if not username:
            return apologize("signup", "Please enter a valid username.")
        if username in sql("users.db", """SELECT username
                                          FROM users""").fetchall()[0]:
            return apologize("signup", "Username already exists. Please choose another username.")


    return render_template("signup.html")


# # Close any open databases
# users_con.close()
# try:
#     notes_con.close()
# except:
#     pass
