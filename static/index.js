import bgColors from "./bgColors.js";
import markdownIt from 'https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/+esm';

document.addEventListener("DOMContentLoaded", () => {
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
    const tool = document.querySelectorAll(".tool");
    const editorTagsContainer = document.getElementById("editor-tags-container");
    const editorTags = document.querySelectorAll(".editor-tags");
    
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
    const noteBodyLabels = ["Note", "Markdown View"]
    try {
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
        
            // Update markdown view's text-align depending on the direction of the text (ltr or rtl)
            var viewAreaDir = window.getComputedStyle(viewArea, null).direction;
            if (viewAreaDir == "rtl") {
                viewArea.style.textAlign = "right";
            }
            else {
                viewArea.style.textAlign = "left";
            }
        });
    }
    // Try/catch prevents viewButton is null errors in no-saving mode
    catch (error) {}
    
    // If the user is logged in (#saving_disabled_message.innerHTML is false), activate autosave
    // I used help from DuckDuckGo AI Chat at duck.ai when implementing the autosave functionality in this project
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
    
    // Function for changing all the background colors to whatever the user wants
    function changeAllColors(colorSource) {
        contentDiv.style.backgroundColor = bgColors[colorSource][0];
        noteData.forEach(colorChange);
        tool.forEach(colorChange);
        editorTags.forEach(colorChange);
        function colorChange(element) {
            if (element.nodeName == "svg") {
                element.style.backgroundColor = bgColors[colorSource][0];
                element.addEventListener("mouseenter", () => {
                    element.style.backgroundColor = bgColors[colorSource][1];
                });
                element.addEventListener("mouseleave", () => {
                    element.style.backgroundColor = bgColors[colorSource][0];
                });
            }
            else {
                element.style.backgroundColor = bgColors[colorSource][1];
            }
        }
    }
    
    // When the user selects a new background color for a note, send a POST request to /autosave to save it and immediately change to that color
    bgSelector.forEach(bgSelectorFunction)
    function bgSelectorFunction(item) {
        const newColor = item.querySelector("p").innerHTML
        item.addEventListener("click", async () => {
            await fetch("/autosave", {
                method: "POST",
                body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": newColor}),
                headers: {"Content-Type": "application/json"}
            });
            changeAllColors(newColor);
        });
    }
    
    // Upon loading a note in the editor, change the note background color according to what's in the database
    try {
        changeAllColors(bgColor);
    }
    // Prevents "Uncaught TypeError: (intermediate value)[bgColor] is undefined"
    catch (error) {}
    
    // Send a POST request to delete a tag when clicking on it, and make the tag disappear from the list of tags
    editorTags.forEach(deleteTag);
    let editorTagsNum = editorTags.length; // Variable used to keep track of the number of tags displayed in the note editor (used for making the tags container invisible when the number of tags reaches zero from deletions)
    function deleteTag(tag) {
        tag.addEventListener("click", async () => {
            await fetch("/tags", {
                method: "POST",
                body: JSON.stringify({"tagTitle": tag.innerHTML, "noteId": noteId.innerHTML}),
                headers: {"Content-Type": "application/json", "Accept": "application/json"}
            });
            editorTagsNum--;
            // Make the tag disappear upon being clicked
            tag.classList.add("invisible");
            // Make the editor tags container disappear when there are no tags left
            if (editorTagsNum == 0) {
                editorTagsContainer.classList.add("invisible");
            }
        });
    }
});
