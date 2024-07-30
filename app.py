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


@app.route("/")
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
                        SELECT note_id, note_title, note_body, bg_color
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


# Route for autosaving notes as the user types
@app.route("/autosave", methods=["POST"])
def autosave():
    # Getting the necessary data
    results = request.get_json()
    date_created = datetime.now().replace(microsecond=0) # TODO
    date_modified = datetime.now().replace(microsecond=0)
    note_id = results.get("note_id")
    note_title = results.get("note_title")
    if note_title == "": note_title = "Untitled note"
    note_body = results.get("note_body")
    first_autosave = results.get("first_autosave")
    bg_color = results.get("bg_color")

    # Try and except to prevent users who aren't logged in from causing errors
    try:
        # If the user is currently updating the background color of the note
        if bg_color:
            # Update the note's background color in the database
            sql(f"./databases/{session.get('username')}-notes.db", 
                """
                UPDATE notes
                SET bg_color = ?,
                    date_modified = ?
                WHERE note_id = ?
                """, (bg_color, date_modified, note_id,))

        # If the user is updating actual note content
        else:
            # If the user is editing a preexisting note (a note ID is received from the client)
            if note_id:
                # If the user updates the title during editing (if a note title is received from the client side)
                if note_title or note_title == "":
                    # Save the new title into the database and update date_modified
                    sql(f"./databases/{session.get('username')}-notes.db", 
                        """
                        UPDATE notes
                        SET note_title = ?,
                            date_modified = ?
                        WHERE note_id = ?
                        """, (note_title, date_modified, int(note_id),))
                
                # If the user updates the body during editing (if a note body is received from the client side)
                elif note_body or note_body == "":
                    # Save the new body into the database and update date_modified
                    sql(f"./databases/{session.get('username')}-notes.db", 
                        """
                        UPDATE notes
                        SET note_body = ?,
                            date_modified = ?
                        WHERE note_id = ?
                        """, (note_body, date_modified, int(results["note_id"]),))

            # If the user is creating a new note (a note ID is not received from the client)
            else:
                # Get the new note's note_id (the highest existing ID in the database)
                if not first_autosave:
                    highest_id = sql(f"./databases/{session.get('username')}-notes.db", 
                                    """
                                    SELECT note_id
                                    FROM notes
                                    ORDER BY note_id DESC
                                    LIMIT 1
                                    """).fetchone()[0]
                    highest_id = int(highest_id)
                    new_note_id = highest_id
                # When the user inputs a title for the new note
                if note_title or note_title == "":
                    # On first creation: Insert new note with a title into the database
                    if first_autosave:
                        qmarks = (session["user_id"], note_title, "", date_created, date_modified,)
                        sql(f"./databases/{session.get('username')}-notes.db", """
                            INSERT INTO notes (user_id, note_title, note_body, date_created, date_modified)
                            VALUES (?, ?, ?, ?, ?)
                            """, qmarks)
                    
                    # On further edits without leaving the page: Update already existing title
                    elif not first_autosave:
                        sql(f"./databases/{session.get('username')}-notes.db", 
                            """
                            UPDATE notes
                            SET note_title = ?,
                                date_modified = ?
                            WHERE note_id = ?
                            """, (note_title, date_modified, new_note_id,))
                
                # When the user inputs a body for the new note
                elif note_body or note_body == "":
                    # On first creation: Insert new note with a body into the database
                    if first_autosave:
                        qmarks = (session["user_id"], "Untitled note", note_body, date_created, date_modified,)
                        sql(f"./databases/{session.get('username')}-notes.db", """
                            INSERT INTO notes (user_id, note_title, note_body, date_created, date_modified)
                            VALUES (?, ?, ?, ?, ?)
                            """, qmarks)
                    
                    # On further edits without leaving the page: Update already existing body
                    elif not first_autosave:
                        sql(f"./databases/{session.get('username')}-notes.db", 
                            """
                            UPDATE notes
                            SET note_body = ?,
                                date_modified = ?
                            WHERE note_id = ?
                            """, (note_body, date_modified, new_note_id,))
                    
    # "sqlite3.OperationalError: no such table: notes" = logged out user trying to edit notes
    except sqlite3.OperationalError:
        return "", 400

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
    

# Display the user's saved notes and delete any empty ones in the database
@app.route("/notes")
@login_required
def notes():
    # Keep track of whether empty notes were deleted or not (True = deletion = reread the notes from the database)
    empty_notes_deleted = False
    # Get the notes from the user's notes database
    notes = sql(f"./databases/{session.get('username')}-notes.db", """
            SELECT note_id, note_title, note_body, bg_color
            FROM notes
            ORDER BY date_created DESC
            """).fetchall()
    
    # Delete any existing empty notes
    for note in notes:
        if note[1] == "Untitled note" and not note[2]:
            sql(f"./databases/{session.get('username')}-notes.db",
                """
                DELETE FROM notes
                WHERE note_id = ?
                """, (note[0],))
            empty_notes_deleted = True
    
    if empty_notes_deleted:
        # Reread the notes from the user's notes database (to get rid of deleted notes)
        notes = sql(f"./databases/{session.get('username')}-notes.db", """
                SELECT note_id, note_title, note_body, bg_color
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
                                bg_color TEXT DEFAULT 'dark' NOT NULL,
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
