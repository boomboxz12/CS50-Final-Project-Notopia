// Get the DOMs
const noteTitle = document.getElementById("title");
const noteBody = document.getElementById("note");
const undoButton = document.getElementById("undo_button");
const redoButton = document.getElementById("redo_button");
const noteId = document.getElementById("note_id");

// Is the user logged in?
const loggedIn = !Boolean(document.getElementById("saving_disabled_message").innerHTML);

// Execute the command "undo" on noteBody when undoButton is clicked (undo change functionality)
undoButton.addEventListener("click", () => {
    noteBody.focus();
    document.execCommand("undo");
})

// Execute the command "redo" on noteBody when redoButton is clicked (redo change functionality)
redoButton.addEventListener("click", () => {
    noteBody.focus();
    document.execCommand("redo");
})

// If the user is logged in (#saving_disabled_message.innerHTML is false), activate autosave
if (loggedIn) {
    // Is this the first autosave on this page visit?
    var firstAutosave = true;
    // Use Fetch API to send the note title to the server every time the user changes the value of noteTitle (for autosave functionality)
    noteTitle.addEventListener("input", async () => {
        await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "note_title": noteTitle.value, "first_autosave": firstAutosave}),
        headers: {"Content-Type": "application/json"}
    });
    // It is no longer the first autosave from now on
    firstAutosave = false;
    });

    // Use Fetch API to send the note body to the server every time the user changes the value of noteBody (for autosave functionality)
    noteBody.addEventListener("input", async () => {
        await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "note_body": noteBody.value, "first_autosave": firstAutosave}),
        headers: {"Content-Type": "application/json"}
    });
    // It is no longer the first autosave from now on
    firstAutosave = false;
    });
}
