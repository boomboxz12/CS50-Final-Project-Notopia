import bgColors from "./bgColors.js"

// Get the DOMs
const notes = document.querySelectorAll(".note-flex-item")
const bgColor = document.getElementById("bg_color");

// Change the colors of the notes in te notes grid according to the database's "bg_color" column
notes.forEach((colorChange))
function colorChange(note) {
    const bgColor = note.querySelector("#bg_color").innerHTML;
    if (bgColor == "dark") {
        note.style.backgroundColor = bgColors[bgColor][2];
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = bgColors[bgColor][3];
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = bgColors[bgColor][2];
        });
    }

    else {
        note.style.backgroundColor = bgColors[bgColor][0];
        note.addEventListener("mouseenter", () => {
            note.style.backgroundColor = bgColors[bgColor][1];
        });
        note.addEventListener("mouseleave", () => {
            note.style.backgroundColor = bgColors[bgColor][0];
        });
    }
}
