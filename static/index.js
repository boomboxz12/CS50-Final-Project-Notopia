import bgColors from "./bgColors.js";
import markdownIt from 'https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/+esm';

// Get the DOMs
const noteTitle = document.getElementById("title");
const noteBody = document.getElementById("note");
const undoButton = document.getElementById("undo_button");
const redoButton = document.getElementById("redo_button");
const noteId = document.getElementById("note_id");
const contentDiv = document.getElementById("content");
const noteData = document.querySelectorAll(".note_data");
const bgSelector = document.querySelectorAll(".bg-selector");
const bgColor = document.getElementById("bg_color").innerHTML;
const viewButton = document.getElementById("view_button");
const viewArea = document.getElementById("view_area");
const noteBodyLabel = document.getElementById("note_body_label");

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

// Toggle editing mode and markdown viewing mode when viewButton is clicked
var viewButtonClicks = 0;
const displayStates = ["inline-block", "none"];
const noteBodyLabels = ["Note", "Markdown view"]
viewButton.addEventListener("click", () => {
    viewButtonClicks += 1;
    // viewArea.style.maxHeight = noteBody.offsetHeight + "px";
    noteBody.style.display = displayStates[viewButtonClicks % 2];
    viewArea.style.display = displayStates[(viewButtonClicks + 1) % 2];
    noteBodyLabel.innerHTML = noteBodyLabels[viewButtonClicks % 2];

    // Update markdown view
    const md = markdownIt();
    const result = md.render(noteBody.value);
    viewArea.innerHTML = result;
});

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

// When the user selects a new background color for a note, send a POST request to /autosave to save it and immediately change to the color
bgSelector.forEach(bgSelectorFunction)
function bgSelectorFunction(item) {
    const newColor = item.querySelector("p").innerHTML
    item.addEventListener("click", async () => {
        await fetch("/autosave", {
            method: "POST",
            body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": newColor}),
            headers: {"Content-Type": "application/json"}
        });
        contentDiv.style.backgroundColor = bgColors[newColor][0];
        noteData.forEach((colorChange))
        function colorChange(element) {
            element.style.backgroundColor = bgColors[newColor][1];
        }
    });
}

// Upon loading a note in the editor, change the note background color according to what's in the database
try {
    contentDiv.style.backgroundColor = bgColors[bgColor][0];
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = bgColors[bgColor][1];
}}
// Prevents "Uncaught TypeError: (intermediate value)[bgColor] is undefined"
catch (error) {}
