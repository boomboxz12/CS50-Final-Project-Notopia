import re
import sqlite3

from flask import flash, Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # User reached route via GET
    if request.method == "GET":
        # If the user is already logged in, redirect them to / instead
        try:
            if session["user_id"]:
                return redirect("/")

        # If not, take them to the login page
        except KeyError:
            return render_template("login.html")

    # User reached route via POST
    if request.method == "POST":
        # Receive the user's information
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if a username was entered
        if not username:
            return apologize("login", "Please enter your username.")
        
        # Check if a password was entered
        if not password:
            return apologize("login", "Please enter your password.")
        
        # Get userdata from users.db
        user = sql("users.db", 
                   """
                   SELECT *
                   FROM users
                   WHERE username = ?
                   """, (username,)).fetchall()
        
        print(len(user))###
        
        # If the user is not found, inform the user
        if not user:
            return apologize("login", """Incorrect username or password. Make sure you entered the correct
                             credintials and try again. If you don't have an account, please make one first.""")
        
        # In the unlikely case that there are multiple users with the same name (normally impossible)
        if len(user) > 1:
            return apologize("login")
        
        # Check the password hash and apologize if it doesn't match
        if not check_password_hash(user[0][2], password):
            return apologize("login", """Incorrect username or password. Make sure you entered the correct
                             credintials and try again. If you don't have an account, please make one first.""")
        
        # If everything is ok, log the user in by remembering their information in flask.session
        session["user_id"] = user[0][0]
        session["username"] = user[0][1]

        # Inform the user that they are now logged in
        flash(f"User {username} logged in!")

        return redirect("/")
    


@app.route("/logout")
def logout():
    # If the user is logged in, forget their session data and inform them
    try:
        # Remember the message before clearing the session data
        flash_message = "User " + session["username"] + " logged out!"

        # Clear the user's session data
        session.clear()

        # Inform the user
        flash(flash_message)
    
    # If they aren't logged in, take them to the login page instead
    except KeyError:
        return redirect("/login")

    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # User reached route via GET
    if request.method == "GET":
        # If the user is already logged in, redirect them to / instead
        try:
            if session["user_id"]:
                return redirect("/")

        # If not, take them to the sign up page
        except KeyError:
            return render_template("signup.html")


    # User reached route via POST
    if request.method == "POST":
        # Receive the user's information
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the username is valid
        if not username:
            return apologize("signup", "Please enter a valid username.")
        
        # Check if the password is valid
        if not password:
            return apologize("signup", "Please enter a valid password.")
        
        # Check if the password contains at least an uppercase letter, at lease a lowercase letter,
        # at lease a number, and is at least 8 characters long
        if not re.fullmatch("^((?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,})$", password):
            return apologize("signup", "Please enter a valid password.")
        
        # Check if the confirmation matches the password
        if confirmation != password:
            return apologize("signup", "The passwords don't match.")

        # Try to add the user to the database
        try:
            sql("users.db", """
                INSERT INTO users (username, hash)
                VALUES (?, ?)
                """, (username, generate_password_hash(password),))
            
        # If an IntegrityError is encountered (i.e., the username is taken), inform the user with an error
        except sqlite3.IntegrityError:
            return apologize("signup", "This username is taken. Please choose another one.")

        # Inform the user that they have been signed up
        flash(f"Account {username} signed up!")
        return redirect("/login")

    return render_template("signup.html")
