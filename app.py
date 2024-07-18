import re
import sqlite3

from datetime import datetime
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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # User reached route via GET
    if request.method == "GET":
        # Read the user's notes and their images
        with sqlite3.connect(f"./databases/{session['username']}-notes.db") as notes_con:
            with sqlite3.connect(f"./databases/{session['username']}-images.db") as images_con:
                notes_cur = notes_con.cursor()
                notes = notes_cur.execute("""
                                          SELECT * FROM notes
                                          """).fetchall()
                images_cur = images_con.cursor()
                images = images_cur.execute("""
                                            SELECT * FROM images
                                            """).fetchall()
                
    # User reached route via POST
    if request.method == "POST":
        # Collect data for processing and saving into the database
        user_id = session["user_id"]
        note_title = request.form.get("note_title")
        note_body = request.form.get("note_body")
        date_created = datetime.now()
        date_modified = datetime.now()
        # A tuple for inserting data into the database
        values = (user_id, note_title, note_body, date_created, date_modified,)
        with sqlite3.connect(f"./databases/{session['username']}-notes.db") as notes_con:
            with sqlite3.connect(f"./databases/{session['username']}-images.db") as images_con:
                notes_cur = notes_con.cursor()
                notes = notes_cur.execute("""
                                          INSERT INTO notes (user_id, note_title, note_body, date_created, date_modified)
                                          VALUES (?, ? , ?, ?, ?)
                                          """, values)
                images_cur = images_con.cursor()
                images = images_cur.execute("""
                                            SELECT * FROM images
                                            """).fetchall()
        return redirect("/")
            
    return render_template("index.html", notes=notes)


@app.route("/login", methods=["GET", "POST"])
def login():
    # User reached route via GET
    if request.method == "GET":
        # If the user is already logged in, redirect them to / instead
        if session.get("user_id"):
            flash("You are already logged in. To log in from another account, please log out first.")
            return redirect("/")

        # If not, take them to the login page
        else:
            # URL used to offer the user to sign up if they haven't already
            signup_url = url_for("signup")
            return render_template("login.html", signup_url=signup_url)

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
    # If the user is logged in, forget their session data and inform them, then redirect to /login
    if session.get("username") is not None:
        # Remember the message before clearing the session data
        flash_message = "User " + session["username"] + " logged out!"

        # Clear the user's session data
        session.clear()

        # Inform the user
        flash(flash_message)

        # Redirect them to /login
        return redirect("/login")
    
    # If they aren't logged in, take them to the login page instead
    else:
        flash("You are not currently logged in.")
        return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # User reached route via GET
    if request.method == "GET":
        # If the user is already logged in, redirect them to / instead
        if session.get("user_id"):
            flash("You are already logged in to an account. To to make a new account, please log out first.")
            return redirect("/")

        # If not, take them to the sign up page
        else:
            login_url = url_for("login")
            return render_template("signup.html", login_url=login_url)


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

        # Try to add the user to the users database
        try:
            sql("users.db", """
                INSERT INTO users (username, hash)
                VALUES (?, ?)
                """, (username, generate_password_hash(password),))
            
            # Make a database for the user's notes and another for images
            with sqlite3.connect(f"./databases/{username}-notes.db") as con:
                cur = con.cursor()
                cur.execute("""
                            CREATE TABLE notes
                            (
                                note_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                user_id INTEGER NOT NULL,
                                note_title TEXT,
                                note_body TEXT,
                                date_created NUMERIC NOT NULL,
                                date_modified NUMERIC NOT NULL,
                                formatting TEXT,
                                color TEXT,
                                bg_color TEXT,
                                tags TEXT,
                                trashed INTEGER DEFAULT 0
                            );
                            """)
            with sqlite3.connect(f"./databases/{username}-images.db") as con:
                cur = con.cursor()
                cur.execute("""
                            CREATE TABLE images
                            (
                                image_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                note_id INTEGER NOT NULL,
                                image BLOB NOT NULL,
                                FORIEGN KEY note_id REFERENCES notes(note_id)
                            );
                            """)
            
        # If an IntegrityError is encountered (i.e., the username is taken), inform the user with an error
        except sqlite3.IntegrityError:
            return apologize("signup", "This username is taken. Please choose another one.")

        # Inform the user that they have been signed up
        flash(f"Account {username} signed up!")
        return redirect("/login")

    return render_template("signup.html")
