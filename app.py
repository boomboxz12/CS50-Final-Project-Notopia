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
def index():
    # Receive arguments
    note_id = request.args.get("id")
    delete_note = request.args.get("del")

    # Get the current user's ID (if any)
    user_id = session.get("user_id")

    # If the user is not logged in, put them in no saving mode (variable used in index.html)
    if not user_id:
        logged_in = False
    else:
        logged_in = True

    

    # User reached route via GET
    if request.method == "GET":
        # try except to prevent users who aren't logged in from causing errors
        try:
            # If the del argument is found, delete the note TODO: DELETE IMAGES
            if delete_note:

                # Reading the note title for the flash message
                note_title = sql(f"./databases/{session['username']}-notes.db",
                                """
                                SELECT note_title
                                FROM notes
                                WHERE note_id = ?
                                """, (delete_note,)).fetchall()[0][0]
                
                # Dots used when the note title is too long for the flash messages
                if len(note_title) > 20:
                    dots = "..."
                else:
                    dots = ""
                
                # Delete the note
                sql(f"./databases/{session['username']}-notes.db",
                    """
                    DELETE FROM notes
                    WHERE note_id = ?
                    """, (delete_note,))
                
                flash(f"""Note "{note_title[:20]}{dots}" deleted!""")

                return redirect("/notes")
            # If there is only an id argument in the URL, then try viewing the note in editing mode
            elif note_id:
                try:
                    note = sql(f"./databases/{session['username']}-notes.db",
                            """
                            SELECT note_id, note_title, note_body
                            FROM notes
                            WHERE note_id = ?
                            """, (note_id,)).fetchall()
                # KeyError = Not logged in
                except KeyError:
                    return apologize("/", "Please log in first.")
            else:
                note = None
        # KeyError = Not logged in
        except KeyError:
            return apologize("/", "Please log in first.")
        # IndexError = Note not found
        except IndexError:
            return apologize("/", "Note not found.", 404)
        
        # If a note with that ID was found, view it
        if note:
            return render_template("index.html", note=note, editing_mode=bool(note_id), logged_in=logged_in)
        # If a note with that ID wasn't found, view it
        elif note == []:
            return apologize("/", "Note not found.", 404)
        # If the user is not trying to access / in editing mode, render the template without the note
        else:
            return render_template("index.html", editing_mode=bool(note_id), logged_in=logged_in)
                
    # User reached route via POST
    if request.method == "POST":
        # try except to prevent users who aren't logged in from causing errors
        try:
            # Collect data for processing and saving into the database
            
            if request.form.get("note_title"):
                # If the user enters a note title, use that as the note title to save in the database
                note_title = request.form.get("note_title")
            else:
                # Otherwise, the default name for notes without a title should be "Untitled note"
                note_title = "Untitled note"

            note_body = request.form.get("note_body")
            date_created = datetime.now().replace(microsecond=0)
            date_modified = datetime.now().replace(microsecond=0)

            # Dots used when the note title is too long for the flash messages
            if len(note_title) > 20:
                dots = "..."
            else:
                dots = ""

            if len(note_title) < 1 and len(note_body) < 1:
                return apologize("/", "You can't save an empty note.")
            
            # If the user is currently editing an already existent note, update it in the database and don't make a new one
            elif note_id: # TODO: CAN'T UPDATE ALL COLUMNS TILL FORMATTING, ETC ARE IMPLEMENTED
                # Only allow saving if the user is logged in
                if logged_in:
                    # A tuple for inserting data into the database (editing)
                    qmarks = (note_title, note_body, date_modified, note_id,)

                    # Update the note's data
                    sql(f"./databases/{session['username']}-notes.db",
                        """
                        UPDATE notes
                        SET note_title = ?,
                            note_body = ?, 
                            date_modified = ?
                        WHERE note_id = ?
                        """, qmarks)
                    
                    flash(f"""Note "{note_title[:20]}{dots}" edited!""")

                    return redirect(f"/?id={note_id}")
                else:
                    return apologize("/", "You are not currently logged in, so saving has been disabled.")

            # If the user is not currently editing an already existent note, create a new one and write it to the database
            else:
                # Only allow saving if the user is logged in
                if logged_in:
                    with sqlite3.connect(f"./databases/{session['username']}-notes.db") as notes_con:
                        with sqlite3.connect(f"./databases/{session['username']}-images.db") as images_con:
                            notes_cur = notes_con.cursor()

                            # A tuple for inserting data into the database (creation)
                            qmarks = (user_id, note_title, note_body, date_created, date_modified,)

                            # Write the new note's data
                            notes = notes_cur.execute("""
                                                    INSERT INTO notes (user_id, note_title, note_body, date_created, date_modified)
                                                    VALUES (?, ? , ?, ?, ?)
                                                    """, qmarks)
                    
                    flash(f"""Note "{note_title[:20]}{dots}" created!""")

                    return redirect("/notes")
                else:
                    return apologize("/", "You are currently not logged in, so saving has been disabled.")
        # KeyError = Not logged in
        except KeyError:
            return apologize("/", "Please log in first.")


    return render_template("index.html")


# Route for autosaving notes as the user types
@app.route("/autosave", methods=["POST"])
def autosave():
    # Getting the necessary data
    results = request.get_json()
    date_created = datetime.now().replace(microsecond=0) # TODO
    date_modified = datetime.now().replace(microsecond=0)
    # If the user updates the title
    if results.get("note_title") and results.get("note_id"):
        # Save the new title into the database and update date_modified
        sql(f"./databases/{session.get('username')}-notes.db", 
            """
            UPDATE notes
            SET note_title = ?,
                date_modified = ?
            WHERE note_id = ?
            """, (results["note_title"], date_modified, int(results["note_id"]),))
    # If the user updates the body
    if results.get("note_body") and results.get("note_id"):
        # Save the new title into the database and update date_modified
        sql(f"./databases/{session.get('username')}-notes.db", 
            """
            UPDATE notes
            SET note_body = ?,
                date_modified = ?
            WHERE note_id = ?
            """, (results["note_body"], date_modified, int(results["note_id"]),))

    # The function returns 204 No Content (A response without a body)
    return "", 204


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
        
        # If the user is not found, inform the user
        if not user:
            return apologize("login", """Incorrect username or password. Make sure you entered them correctly and
                             try again. If you don't have an account, please make one first. Note that usernames
                            and passwords are case sensitive.""")
        
        # In the unlikely case that there are multiple users with the same name (normally impossible)
        if len(user) > 1:
            return apologize("login")
        
        # Check the password hash and apologize if it doesn't match
        if not check_password_hash(user[0][2], password):
            return apologize("login", """Incorrect username or password. Make sure you entered them correctly and
                             try again. If you don't have an account, please make one first. Note that usernames
                            and passwords are case sensitive.""")
        
        # If everything is ok, log the user in by remembering their information in flask.session
        session["user_id"] = user[0][0]
        session["username"] = user[0][1]

        # Inform the user that they are now logged in
        flash(f'User "{username}" logged in!')

        return redirect("/notes")
    


@app.route("/logout")
def logout():
    # If the user is logged in, forget their session data and inform them, then redirect to /login
    if session.get("username") is not None:
        # Remember the message before clearing the session data
        flash_message = "User " + '"' + session["username"] + '"' + " logged out!"

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
    

# Display the user's saved notes
@app.route("/notes")
@login_required
def notes():
    # Get the notes from the user's notes database
    notes = sql(f"./databases/{session.get('username')}-notes.db", """
            SELECT note_id, note_title, note_body
            FROM notes
            ORDER BY date_created DESC
            """).fetchall()
    
    return render_template("notes.html", notes=notes)

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
        flash(f'Account "{username}" signed up!')

        return redirect("/login")

    return render_template("signup.html")
