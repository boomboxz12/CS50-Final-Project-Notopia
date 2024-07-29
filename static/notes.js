// Get the DOMs
const notes = document.querySelectorAll(".note-flex-item")
const bgColor = document.getElementById("bg_color");

// Change the colors of the notes in te notes grid according to the database's "bg_color" column
notes.forEach((colorChange))
function colorChange(note) {
    if (note.querySelector("#bg_color").innerHTML == "dark") {
        note.style.backgroundColor = "#2c2c2c";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#393939";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#2c2c2c";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "red") {
        note.style.backgroundColor = "#361617";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#481d1e";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#361617";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "orange") {
        note.style.backgroundColor = "#463123";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#554032";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#463123";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "yellow") {
        note.style.backgroundColor = "#453b22";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#4c4228";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#453b22";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "green") {
        note.style.backgroundColor = "#28381e";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#2f4224";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#28381e";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "aqua") {
        note.style.backgroundColor = "#1a3639";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#1f4546";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#1a3639";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "navy") {
        note.style.backgroundColor = "#2a3137";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#32393f";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#2a3137";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "blue") {
        note.style.backgroundColor = "#232a3d";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#2e3854";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#232a3d";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "purple") {
        note.style.backgroundColor = "#302533";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#3a2b40";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#302533";
        });
    }

    else if (note.querySelector("#bg_color").innerHTML == "pink") {
        note.style.backgroundColor = "#451926";
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = "#5c2233";
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = "#451926";
        });
    }
}