// Get the DOMs
const noteTitle = document.getElementById("title");
const noteBody = document.getElementById("note");
const deleteNoteButton = document.getElementById("delete_note")
const undoButton = document.getElementById("undo_button")
const redoButton = document.getElementById("redo_button")
const noteId = document.getElementById("note_id")

// Only allow saving if the user is logged in
// If element #submit is null, then the element doesn't exist because the user is not logged in (as per index.html)
if (document.getElementById("submit") != null) {
    const submit = document.getElementById("submit");
    // Interval for enabling the save note button only if something is entered in either the title or the body fields
    setInterval(() => {
        if (noteTitle.value.length >= 1 || noteBody.value.length >= 1) {
            submit.removeAttribute("disabled");
            submit.removeAttribute("tabindex");
            submit.removeAttribute("aria-disabled");
        }
        
        else {
            submit.setAttribute("disabled", "disabled");
            submit.setAttribute("tabindex", "-1");
            submit.setAttribute("aria-disabled", "true");
        }
    }, 10);
}

// Using BeforeUnloadEvent to warn the user if they leave the page without saving
// const titleValue = noteTitle.value;
// const bodyValue = noteBody.value;
// let submitted = false;
// window.onbeforeunload = function() {
//     if (!submitted) {
//         if (noteTitle.value != titleValue || noteBody.value != bodyValue) {
//             return "You have unsaved changes. Are you sure you want to leave?";
//         }
// }}

// Execute the command "undo" on noteBody when undoButton is clicked (undo change functionality)
undoButton.addEventListener("click", () => {
    noteBody.focus()
    document.execCommand("undo")
})

// Execute the command "redo" on noteBody when redoButton is clicked (redo change functionality)
redoButton.addEventListener("click", () => {
    noteBody.focus()
    document.execCommand("redo")
})

// Use Fetch API to send the note title to the server every time the user changes the value of noteTitle (for autosave functionality)
noteTitle.addEventListener("input", async () => {
    await fetch("/autosave", {
    method: "POST",
    body: JSON.stringify({"note_id": noteId.innerHTML, "note_title": noteTitle.value}),
    headers: {"Content-Type": "application/json"}
})});

// Use Fetch API to send the note body to the server every time the user changes the value of noteBody (for autosave functionality)
noteBody.addEventListener("input", async () => {
    await fetch("/autosave", {
    method: "POST",
    body: JSON.stringify({"note_id": noteId.innerHTML, "note_body": noteBody.value}),
    headers: {"Content-Type": "application/json"}
})});