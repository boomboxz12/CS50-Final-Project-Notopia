
# Notopia
#### Video Demo: [Notopia - CS50x 2024 Final Project by Ahmed Mansour (YouTube)](https://youtu.be/b7D6ZoaX_pI)
#### Description: A simple note-taking web app made with Flask.

## What can *Notopia* do?
***Notopia*** is your new favorite note-taking app that combines simplicity and ease of use with flexibility and features. It's a basic note-taking app that is designed to get out of your way and help you focus on what matters.

## An overview of *Notopia*'s features
Creating a Notopia account unlocks a wide range of features, such as the ability to **save** notes, use ***Markdown*** in your notes, choose **note background colors**, create and manage **tags**, and more!

### No-saving mode
Without an account, you are limited to what I call ***No-saving mode***, where you can write a quick textual note without saving or any extra features. Think needing to just quickly write a piece of information that's only relevant for that very moment, such as small sequences of letters or numbers that you want to be able to easily see for a few minutes as you work with it without the need to save it. *Notopia* Won't get in your way and force you to make an account just for that. Just work away!

To access the rest of *Notopia*'s multitude of features, a **_Notopia_ account** is required. It's free and easy to make—just choose a username and a password and you're off!

### The *Notopia* note editor
The *Notopia* note editor is where you do all the note-taking. There, you can create new notes and view/edit existing ones. You can give each note a title and a body of text. **Right-to-Left (RTL)** languages are also supported and render properly.

#### *Notopia* autosaves notes for you!
No need to worry about saving your notes in *Notopia*! The note editor is equipped with an **autosave** function. Any single modification you make to the title, the body, or even the background color gets saved in a flash!

#### Helpful tools in the note editor
Below the Note body field in the editor, you can find a few tools to help you with note writing/editing and organization.

The first two of these editor tools are the **Undo** and **Redo** tools, which work exactly as you would expect and make it easier for mobile users to access these functions without needing to use keyboard shortcuts like ctrl+z or ctrl+y, making their lives easier.

Then comes the **Markdown View Toggler**. Using this tool, you can toggle between the note body field (for editing) and *Markdown View* (for viewing *Markdown*). With the simple *Markdown* syntax, you can add a touch of **formatting** to your text, as well as **hyperlinks**, **images**, and more! It's worth noting that *Markdown* is not specific to *Notopia*. For more information about *Markdown* and its syntax, search for "*Markdown*" with your favorite search engine.

Next to that is the **Note Background Color Selector**. It can be used to change the note's background color to any of 10 provided colors. It can be used for **color-coding notes** that have things in common, or it can be used to make notes more aesthetically pleasing according to your taste. The choice is yours, so get painting!

And last but not least, the **Delete Note** tool. If you don't need a note anymore, you can use this tool to delete it from your account's database.

### Your notes, listed beautifully
Next up is the ***My notes*** page. There, you can see a list of every note you have created, minus the ones you may have deleted.

On this page, the notes appear in a lovely **grid view**, and you can even peek at their titles/bodies without having to open them. Note background colors also show up here, allowing you to color-code specific notes according to your needs. Clicking or tapping a note opens it in the editor for editing and viewing.

Each note has a checkbox on its top left corner. To **select multiple notes**, simply check the checkboxes of the notes you would like to select. This way, you can **delete notes in bulk*** or **link them to a tag or tags** for organization (I'll explain tags below!). Pure time-saving here!

Your list of notes is sorted by creation date (descending) by default. Don't prefer that? No problem! **Sort your notes** as you like with the ***Sort tool*** at the top to help you get to what you need as quickly as possible.

Ok, your notes are sorted as you like. Still don't think it's enough? I've provided you with the ***Filter tool***, which allows you to **choose a tag or tags to only show the notes linked to them**. Whether the note you're looking for is about work, entertainment, or family, it's as simple as choosing a tag or tags to show only the notes linked to them!

Finding notes has never been easier with the ***Search tool***, which enables you to find a note based on text in its title or body. That's three tools to help you get to notes easier and increase your productivity. Three!

### Need to organize? Tags are here to help!
After that is the ***My tags*** page, your hub for anything tags! With it, you can **view** your created tags and the notes linked with them, **create** new tags, **rename** existing tags, and **delete** the tags you no longer need.

Tags can be thought of as folders where your notes can be grouped for organization, except a single note can be linked to multiple tags at the same time. A note about my son's health would go in both a "Family" tag and a "Health" tag for better organization. This way, I can filter my notes by a specific tag or tags (as explained above) for **quick access to all the notes about a specific topic**.

If you feel the need to **change your password** or get a **backup copy** of the database file containing your notes and tags, head to ***Account settings*** and you won't be disappointed!

## Behind the scenes
*Notopia* was constructed with the help of 8 technologies, namely HTML, CSS, Bootstrap, JavaScript, Python, Flask, Jinja, and SQLite. Below, I go through everything I used and every file and how they all contribute together to form *Notopia*.

### The skeleton
Composing *Notopia*'s skeleton are 9 **HTML** files, all located in the *templates* folder. Most of them are self-explanatory, such as *account.html*, *help.html*, *login.html*, *mytags.html*, *notes.html*, and *signup.html*.

In addition, there's also *error.html* (which is responsible for rendering all errors), index.html (which is the note editor), and *layout.html* (which is the base on which all other HTML files build, as it contains all shared components that other HTML files use).

### The paint
**CSS** is the beautifier at play here. I used it to style my elements, customize Bootstrap components, and make my app responsive so it can scale to all display sizes/resolutions used in 2024. In the *static* folder are the 750+ lines of CSS code that make *Notopia* as visually appealing as it is.

### Making *Notopia* interactive
To add interactivity to my pages, I used **JavaScript**. 7 JavaScript files live in the *static* folder as they provide essential functionality, mostly (but not exclusively) related to client-side checks for the forms.

Each JavaScript file is named after the HTML file/route it works with, including *account.js*, *index.js*, *login.js*, *mytags.js*, *notes.js*, and *signup.js*. The only exception is *account.html*, which uses both *account.js* and *signup.js* (due to the similarities between the form used for signing up and the form used for changing the user's password).

As well, *bgColors.js* is one file that does a lot of the heavy lifting for *index.js* and *notes.js* by providing them with the colors needed to render colored notes properly, reducing the redundancy that could result from having the same code exist in these two files.

### *Notopia*'a identity
Two .png files can also be found in the static folder, *lines-7129047_1280.png* and *Notopia Logo.png*. While the logo is obvious, the lines file is used as the cozy background that the user sees behind the page content.

### The brain
The brain behind Notopia's logic is *app.py*, the main Python file that controls the entire server. Assisting it is *helpers.py*, which contains some helper functions, including *login_required* (used to restrict access to protected pages), *apologize* (used to render an error) and *sql* (used to enable most interactions with the databases), which I use extensively throughout the app. Alongside *app.py* is *requirements.txt*, which lists the external components I use in *Notopia*, all of which can be installed with *pip*.

### How *Notopia* "remembers"
*users.db*, the file Notopia creates upon the creation of the first user/account, is located in the root directory. It's a simple database with only one table where the username, as well as a password hash (but not the plain password itself) get stored.

The *databases* directory is where all users' databases go. Each user has their own database, containing three tables (one table for the notes, another table for the tags, and the third table is used to faciliate the many-to-many relationship between notes and tags).

## Closing words
That's about all you need to know to use *Notopia*, the clean and simple web-based note-taking app. Feel free to explore around now and see how *Notopia* is capable of helping you!

I hope the above "Behind the scenes" section explains how *Notopia* works as clearly and cleanly as possible.

This app was created by me (and me alone!) in 2024 for the ***CS50x 2024 Final Project***. Wish me luck!
