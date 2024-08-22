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
        # If the del argument is found, delete the note
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
            
            flash(f"""Note "{note_title[:20]}{dots}" deleted.""")

            return redirect("/notes")
        
        # If there is only an id argument in the URL (no del argument), then try reading the note from the database
        elif note_id:
            try:
                note = sql(f"./databases/{session['username']}-notes.db",
                        """
                        SELECT note_id, note_title, note_body, bg_color, date_created, date_modified
                        FROM notes
                        WHERE note_id = ?
                        """, (note_id,)).fetchall()
                note[0] = list(note[0])
            # KeyError = Not logged in
            except KeyError:
                return apologize("/", "Please log in first.")
            
            # Read the note's tags from the database
            note_tags = sql(f"./databases/{session['username']}-notes.db", 
                             """
                             SELECT tag_title
                             FROM tags
                             WHERE tag_id IN (
                                                SELECT tag_id
                                                FROM tags_notes
                                                WHERE note_id = ?
                                            )
                             ORDER BY tag_title COLLATE NOCASE ASC
                             """, (note_id,)).fetchall()
            
            # List for converting note_tags into a list of elements each of which is one of the note's tags
            note_tags_list = []

            # Place each tag into the list above
            for i in note_tags:
                note_tags_list.append(i[0])

            # Place the tags list into the note variable
            note[0].append(note_tags_list)

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
    # If a note with that ID wasn't found, apologize
    elif note == []:
        return apologize("/", "Note not found.", 404)
    # If the user is not trying to access index (/) in editing mode, render the template without the note
    else:
        return render_template("index.html", editing_mode=bool(note_id), logged_in=logged_in)


# Route for autosaving notes as the user types
@app.route("/autosave", methods=["POST"])
@login_required
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

        return redirect("/notes")
    

@app.route("/logout")
def logout():
    # If the user is logged in, forget their session data then redirect to /login
    if session.get("username") is not None:
        # Clear the user's session data
        session.clear()

        # Redirect them to /login
        return redirect("/login")
    
    # If they aren't logged in, take them to the login page instead
    else:
        flash("You are not currently logged in.")
        return redirect("/login")
    

# Lets the user see their tags and the notes linked with them, create empty tags, rename existing tags, and delete tags
@app.route("/mytags")
def mytags():
    # Read the user's tag titles and IDs from their database
    tags = sql(f"./databases/{session.get('username')}-notes.db",
               """
               SELECT tag_title, tag_id
               FROM tags
               ORDER BY tag_title COLLATE NOCASE ASC
               """).fetchall()
    
    print(tags, "TAGSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")###
    
    # A dict where each key is a tag title and each value is a list containing all notes linked with that tag (dict currently empty, will be populated below)
    tags_dict = {}

    for tag in tags:
        # Reach each tag's notes (note titles only)
        notes_in_tag = sql(f"./databases/{session.get('username')}-notes.db",
                        f"""
                        SELECT note_title
                        FROM notes
                        WHERE note_id IN
                        (
                            SELECT note_id
                            FROM tags_notes
                            WHERE tag_id IN
                            (
                                SELECT tag_id
                                FROM tags
                                WHERE tag_title = '{tag[0]}'
                            )
                        )
                        """).fetchall()
        # If the tags_dict dictionary doesn't yet contain a key corresponding to the current tag, create one
        # and assign an empty list as its value (to be populated with note titles later)
        if not tags_dict.get(tag[0]):
            tags_dict[tag[0]] = []
        # For each note linked with the tag we are currently working on...
        for note in notes_in_tag:
            # ... add its title to the list (which is the value assigned to the key representing the current tag being worked on during the current iteration of the parent for loop)
            tags_dict[tag[0]].append(note[0])

    return render_template("mytags.html", tags_dict=tags_dict, tags=tags)


# Display the user's saved notes and delete any empty ones in the database
@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    # Has the user requested that I sort their notes?
    sort = request.args.get("sort_notes_by")

    # Has the user requested that I filter their notes by a tag or tags?
    filter = request.form
    filter_string = ""
    filter_information = ""
    if filter:
        # The number of question marks (parameters) to be passed to the SQL query is equal to the number of keys received
        qmarks = "?, " * len(filter.keys())
        qmarks = qmarks[:-2]
        # A string to be added to the the SQL query under the function get_notes below
        filter_string = f"""
        WHERE note_id IN (
            SELECT note_id
            FROM tags_notes
            WHERE tag_id IN (
                SELECT tag_id
                FROM tags
                WHERE tag_title IN ({qmarks})
            )
        )
        """
        filtered_by = ""
        for i in filter.keys():
            filtered_by += i + ", "
        filtered_by = filtered_by[:-2] + "."
        filter_information = f"Your notes are filtered by the following tags: {filtered_by}"
        

    # Dictionary used to modify the SQL query when sorting notes
    sort_dict = {
        "title-asc": "note_title COLLATE NOCASE ASC",
        "title-desc": "note_title COLLATE NOCASE DESC",
        "creation-asc": "date_created ASC",
        "creation-desc": "date_created DESC",
        "modification-asc": "date_modified ASC",
        "modification-desc": "date_modified DESC",
        None: "date_created DESC"
    }

    # Is the user requesting note multi deletion? If so, which notes should I try to delete?
    try:
        notes_to_delete = tuple(int(i) for i in tuple(request.args.get("del").split(",")))
        # If there are notes to multi delete, delete them from the database
        if notes_to_delete:
            # Placeholder question marks for the SQL query (a number of ?s matching the number of notes to delete)
            qmarks = "?, " * len(notes_to_delete)
            # Delete the last two characters of qmarks (the ", ")
            qmarks = qmarks[:-2]

            # Delete the notes from the database
            deletion_done = bool(sql(f"./databases/{session.get('username')}-notes.db", 
                                     f"""
                                     DELETE FROM notes
                                     WHERE note_id IN ({qmarks})
                                     """, notes_to_delete).rowcount)
            # Only inform the user about deletion(s) after actual deletions (and not when visiting /notes?del=X where X is the ID of a nonexistent note)
            if deletion_done:
                flash("Note(s) deleted.")
                return redirect("/notes")
            
    # AttributeError = note deletion not requested (no args)
    except AttributeError:
        pass
    
    # Read the notes from the user's notes database
    def get_notes():
        notes = sql(f"./databases/{session.get('username')}-notes.db", f"""
                SELECT note_id, note_title, note_body, bg_color, date_created, date_modified
                FROM notes
                {filter_string}
                ORDER BY {sort_dict[sort]}
                """, tuple(filter.keys())).fetchall()
        return notes
    
    # Delete any existing empty notes
    for note in get_notes():
        if note[1] == "Untitled note" and not note[2]:
            sql(f"./databases/{session.get('username')}-notes.db",
                """
                DELETE FROM notes
                WHERE note_id = ?
                """, (note[0],))
            
    tags = sql(f"./databases/{session.get('username')}-notes.db", f"""
               SELECT tag_title
               FROM tags
               ORDER BY tag_title COLLATE NOCASE ASC
               """).fetchall()
                
    return render_template("notes.html", notes=get_notes(), tags=tags, filter_information=filter_information) # Calling get_notes again to reread the notes after deleting any empty notes
    
    
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

        # If users.db doesn't alrady exist, make it
        try:
            sql("users.db", """
                CREATE TABLE users 
                (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    hash TEXT NOT NULL
                )
                """)
        except sqlite3.OperationalError:
            pass

        try:
            # Try to add the user to the users database
            sql("users.db", """
                INSERT INTO users (username, hash)
                VALUES (?, ?)
                """, (username, generate_password_hash(password),))
            
            # Make a database for the user's notes and tags
            with sqlite3.connect(f"./databases/{username}-notes.db") as con:
                cur = con.cursor()
                cur.executescript("""
                                    BEGIN;
                                    CREATE TABLE notes
                                    (
                                        note_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                        user_id INTEGER NOT NULL,
                                        note_title TEXT,
                                        note_body TEXT,
                                        date_created NUMERIC NOT NULL,
                                        date_modified NUMERIC NOT NULL,
                                        bg_color TEXT DEFAULT 'dark' NOT NULL
                                    );
                                    CREATE TABLE tags_notes
                                    (
                                        tag_id INTEGER,
                                        note_id INTEGER,
                                        PRIMARY KEY (tag_id, note_id),
                                        FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
                                        FOREIGN KEY (note_id) REFERENCES notes (note_id)
                                    );
                                    CREATE TABLE tags
                                    (
                                        tag_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                        tag_title TEXT NOT NULL UNIQUE
                                    );
                                    COMMIT;
                                    """)
            
        # If an IntegrityError is encountered (i.e., the username is taken), inform the user with an error
        except sqlite3.IntegrityError:
            return apologize("signup", "This username is taken. Please choose another one.")

        # Inform the user that they have been signed up
        flash(f'Account "{username}" signed up.')

        return redirect("/login")

    return render_template("signup.html")


# Handle tags
@app.route("/tags", methods = ["POST"])
@login_required
def tags():
    source = request.form.get("source") # Used to redirect the user to the page they came from after the tags function finishes

    # If the user is requesting that I rename one of their tags, do the following
    if request.form.get("operation") == "rename":
        tag_id = request.form.get("tag-id")
        if not tag_id:
            return apologize(source)
        new_tag_title = request.form.get("new-tag-title")

        # Only rename the tag if a new tag title was entered
        if new_tag_title:
            # Check if the new tag title is alphanumeric
            if new_tag_title.isalnum():
                # Try updating the tag title in the database
                try:
                    sql(f"./databases/{session['username']}-notes.db",
                        """
                        UPDATE tags
                        SET tag_title = ?
                        WHERE tag_id = ?
                        """, (new_tag_title, int(tag_id)))
                except sqlite3.IntegrityError:
                    return apologize(source, "You can't have more than one tag with the same title.")
            
            # If the new tag title is not alphanumeric, don't update the tag title and apologize to the user
            else:
                return apologize(source, "The tag title you entered is invalid. Please enter a valid tag title to rename your tag.")
        
        # If a new tag title wasn't entered, don't update the tag title and apologize to the user 
        elif not new_tag_title:
            return apologize(source, "The tag title you entered is invalid. Please enter a valid tag title to rename your tag.")
        
    elif request.form.get("operation") == "delete":
        tag_id = request.form.get("tag-id")
        if not tag_id:
            return apologize(source)
        with sqlite3.connect(f"./databases/{session['username']}-notes.db") as con:
            cur = con.cursor()
            cur.execute("BEGIN;")
            cur.execute(
                """
                DELETE FROM tags
                WHERE tag_id = ?
                """, (tag_id,))
            cur.execute(
                """
                DELETE FROM tags_notes
                WHERE tag_id = ?
                """, (tag_id,))
            cur.execute("COMMIT;")



    # Otherwise, if the requested operation is something else, do the following
    else:
        # Creating tags and adding notes to them
        # Receive the tag title(s) entered/selected by the user and the selected notes
        tag_title = request.form.get("tag-title") # Newly created tag(s)
        selected_modal_tags = request.form.get("selected-modal-tags") # Already created tags that are selected by checking the checkmark
        if selected_modal_tags: selected_modal_tags = selected_modal_tags.split(",")
        selected_notes = request.form.get("selected-notes")
        if selected_notes: selected_notes = selected_notes.split(",")
        

        # Initially, the tag_list is empty
        tags_list = []

        # If the new tags are alphanumeric and are separated by spaces, find all regex matches to get a list of just the tags
        try:
            if tag_title and len(tag_title) < 21:
                if tag_title.replace(" ", "").isalnum():
                    tags_list = re.findall("(\w+)[^ ]*", tag_title)
            elif len(tag_title) > 20:
                return apologize(source, "Tag titles can't be longer than 20 characters.")
            
        except TypeError: # Prevents "TypeError: object of type 'NoneType' has no len()"
            pass

        # In the case of missing or invalid new tags, inform the user with an error
        if not tags_list and tag_title:
            return apologize(source, """Please enter a valid title for the tag you want to create.
                            You can also enter multiple titles separated by spaces to create multiple tags.
                            Only alphanumeric characters are allowed in tag titles. Tag titles can't be longer than 20 characters.""")
        
        # Insert newly created tag(s) into the database
        try:
            with sqlite3.connect(f"./databases/{session['username']}-notes.db") as con:
                cur = con.cursor()
                cur.execute("BEGIN;")
                for i in tags_list:
                    cur.execute(
                        """
                        INSERT INTO tags (tag_title)
                        VALUES (?)
                        """, (i,))
                cur.execute("COMMIT;")
        except sqlite3.IntegrityError:
            return apologize(source, "You can't have more than one tag with the same title.")
        
        # Extend the tags_list so it covers both newly created tags and existing tags for association with the selected notes
        if selected_modal_tags: tags_list.extend(selected_modal_tags)

        # Associate the notes with their tags (new and existing) by inserting into tags_notes
        try:
            with sqlite3.connect(f"./databases/{session['username']}-notes.db") as con:
                cur = con.cursor()
                if selected_notes:
                    for i in selected_notes:
                        for j in tags_list:
                            cur.execute(
                                f"""
                                INSERT INTO tags_notes (tag_id, note_id)
                                VALUES ((
                                        SELECT tag_id
                                        FROM tags
                                        WHERE tag_title = '{j}'
                                        ),
                                        {i})
                                """)
        # IntegrityError = The user attempts to add a tag to a note when that tag is already added to the note (associating the note with a tag it's already associated with)
        except sqlite3.IntegrityError:
            return apologize(source, "This note has already been added to that tag.")
        

        # Removing a note from a tag when the tag is clicked when the note is open in the editor
        if request.is_json:
            results = request.get_json()
            tag_title_to_delete = results.get("tagTitle")
            current_note_id = results.get("noteId")

            sql(f"./databases/{session['username']}-notes.db", 
                """
                DELETE FROM tags_notes
                WHERE note_id = ?
                AND tag_id = (
                    SELECT tag_id
                    FROM tags
                    WHERE tag_title = ?
                )
                """, (int(current_note_id), tag_title_to_delete,))

    # If the source of the POST request by which the user reached /tags is /mytags or /notes, redirect them back to the source
    if source in ["/mytags", "/notes"]:
        flash("Tag(s) modified successfully.")
        return redirect(source)
    # Otherwise, if the source is /, return an empty body instead (do nothing) and don't redirect
    else:
        return "", 204
