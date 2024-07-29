// Get the DOMs
const noteTitle = document.getElementById("title");
const noteBody = document.getElementById("note");
const undoButton = document.getElementById("undo_button");
const redoButton = document.getElementById("redo_button");
const noteId = document.getElementById("note_id");
const contentDiv = document.getElementById("content");
const noteData = document.querySelectorAll(".note_data");
const bgSelectorDark = document.getElementById("bg-selector-dark");
const bgSelectorRed = document.getElementById("bg-selector-red");
const bgSelectorOrange = document.getElementById("bg-selector-orange");
const bgSelectorYellow = document.getElementById("bg-selector-yellow");
const bgSelectorGreen = document.getElementById("bg-selector-green");
const bgSelectorAqua = document.getElementById("bg-selector-aqua");
const bgSelectorNavy = document.getElementById("bg-selector-navy");
const bgSelectorBlue = document.getElementById("bg-selector-blue");
const bgSelectorPurple = document.getElementById("bg-selector-purple");
const bgSelectorPink = document.getElementById("bg-selector-pink");
const bgColor = document.getElementById("bg_color");

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

// When the user selects a background color for the note, send a POST request to /autosave to save it and immediately change to the color
bgSelectorDark.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "dark"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#212121";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#343434";
    }
});

bgSelectorRed.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "red"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#361617";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#481d1e";
    }
});

bgSelectorOrange.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "orange"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#463123";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#554032";
    }
});

bgSelectorYellow.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "yellow"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#453b22";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#4c4228";
    }
});

bgSelectorGreen.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "green"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#28381e";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#2f4224";
    }
});

bgSelectorAqua.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "aqua"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#1a3639";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#1f4546";
    }
});

bgSelectorNavy.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "navy"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#2a3137";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#32393f";
    }
});

bgSelectorBlue.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "blue"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#232a3d";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#2e3854";
    }
});

bgSelectorPurple.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "purple"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#302533";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#3a2b40";
    }
});

bgSelectorPink.addEventListener("click", async () => {
    await fetch("/autosave", {
        method: "POST",
        body: JSON.stringify({"note_id": noteId.innerHTML, "bg_color": "pink"}),
        headers: {"Content-Type": "application/json"}
    });
    contentDiv.style.backgroundColor = "#451926";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#5c2233";
    }
});

// Upon loading the note, change the note background color according to what's in the database
if (bgColor.innerHTML == "dark") {
    contentDiv.style.backgroundColor = "#212121";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#343434";
    }
}

else if (bgColor.innerHTML == "red") {
    contentDiv.style.backgroundColor = "#361617";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#481d1e";
    }
}

else if (bgColor.innerHTML == "orange") {
    contentDiv.style.backgroundColor = "#463123";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#554032";
    }
}

else if (bgColor.innerHTML == "yellow") {
    contentDiv.style.backgroundColor = "#453b22";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#4c4228";
    }
}

else if (bgColor.innerHTML == "green") {
    contentDiv.style.backgroundColor = "#28381e";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#2f4224";
    }
}

else if (bgColor.innerHTML == "aqua") {
    contentDiv.style.backgroundColor = "#1a3639";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#1f4546";
    }
}

else if (bgColor.innerHTML == "navy") {
    contentDiv.style.backgroundColor = "#2a3137";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#32393f";
    }
}

else if (bgColor.innerHTML == "blue") {
    contentDiv.style.backgroundColor = "#232a3d";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#2e3854";
    }
}

else if (bgColor.innerHTML == "purple") {
    contentDiv.style.backgroundColor = "#302533";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#3a2b40";
    }
}

else if (bgColor.innerHTML == "pink") {
    contentDiv.style.backgroundColor = "#451926";
    noteData.forEach((colorChange))
    function colorChange(element) {
        element.style.backgroundColor = "#5c2233";
    }
}
