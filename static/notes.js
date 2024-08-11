import bgColors from "./bgColors.js";

// Get the DOMs
const notes = document.querySelectorAll(".note-flex-item");
const selectedNotesCounter = document.getElementById("selected-notes-counter");
const modalBody = document.getElementById("modal-body");
const confirmDelete = document.getElementById("modal-confirm-delete-button");
const confirmLeave = document.querySelectorAll(".confirm-leave");
const sortNotesContainer = document.getElementById("sort-notes-container");
const filterNotesContainer = document.getElementById("filter-notes-container");
const showSortButton = document.getElementById("show-sort-button");
const showFilterButton = document.getElementById("show-filter-button");
const selectedNotesInput = document.getElementById("selected-notes");
const modalTags = document.querySelectorAll(".notes-tag");
const selectedModalTagsInput = document.getElementById("selected-modal-tags");

// Change the colors of the notes in te notes grid according to the database's "bg_color" column
notes.forEach((colorChange))
function colorChange(note) {
    const bgColor = note.querySelector(".bg_color").innerHTML;
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

// Array for keeping track of selected notes
const selectedNotes = [];

// Add selected notes to the array and remove deselected ones
notes.forEach(noteSelector);
function noteSelector(note) {
    // Selecting DOMs
    const note_id = note.querySelector("p").innerHTML;
    const note_checkbox = note.querySelector("input[type=checkbox]");
    const selectedNotesCounterText = selectedNotesCounter.querySelector(".d-flex").querySelector(".toast-body")

    note.addEventListener("input", () => {
        // Add notes with a checked checkbox to the selectedNotes array
        if (note_checkbox.checked) {
            selectedNotes.push(note_id);
        }
        // Remove notes with an unchecked checkbox (that were previously checked) from the selectedNotes array
        else if (!note_checkbox.checked) {
            selectedNotes.splice(selectedNotes.indexOf(note_id), 1);
        }

        // Populate the #selected-notes input element with the selectedNotes array for use when associating notes with tags
        selectedNotesInput.value = selectedNotes;

        // Change href on the modal dialog (confirm deletion) to enable the deletion of selected notes
        confirmDelete.href = "/notes?del=" + selectedNotes;
        
        // Variable to make sure the selected note counter says "note" when it's only one and "notes" when it's more than one
        let s = "";

        // Trigger the selected note counter toast 
        if (selectedNotes.length > 0) {
            selectedNotesCounter.classList.remove("invisible");
            // If there are multiple notes selected, add an s at the end of the word "note". Otherwise, don't do that
            if (selectedNotes.length > 1) {
                s = "s";
            }
            else {
                s = "";
            }
            selectedNotesCounterText.innerHTML = selectedNotes.length + " note" + s + " selected";
            modalBody.innerHTML = "Are you sure you want to delete " + selectedNotes.length + " note" + s + "?<br>This action can't be undone!";
        }
        else {
            selectedNotesCounter.classList.add("invisible");
        }
    });
}

// Make sure the user doesn't accidentally click out of the page when selecting a note or notes
var leavingConfirmed = false; // By default, warn the user when leaving the page when one or more notes are selected unless confrimed
confirmLeave.forEach(dontWarn)
function dontWarn(item) {
    item.addEventListener("click", () => {
        leavingConfirmed = true;
    })
}
window.onbeforeunload = function() {
    // Only warn the user if they have notes selected and if the leavingConfirmed variable is false
    if (!leavingConfirmed) {
        if (selectedNotes.length > 0) {
            return "You currently have a note or more selected. Are you sure you want to leave?";
        }
    }
}

// Show/hide the note sorting/filtering options when clicking the respective button
let displayModes = ["none", "inline"];
let numberOfSortClicks = 0;
let numberOfFilterClicks = 0;
showSortButton.addEventListener("click", () => {
    numberOfSortClicks++;
    numberOfFilterClicks = 0;
    filterNotesContainer.style.display = "none";
    sortNotesContainer.style.display = displayModes[numberOfSortClicks % 2];
});
showFilterButton.addEventListener("click", () => {
    numberOfSortClicks = 0;
    numberOfFilterClicks++;
    filterNotesContainer.style.display = displayModes[numberOfFilterClicks % 2];
    sortNotesContainer.style.display = "none";
});

// Array for keeping track of the tags selected in the "add selected note(s) to tag(s)" modal dialog
let selectedModalTags = [];

// Add selected modal tags to the array and remove deselected ones
modalTags.forEach(modalTagSelector)
function modalTagSelector(modalTagContainer) {
    const tagInput = modalTagContainer.querySelector("input");
    const tagLabel = modalTagContainer.querySelector("label");
    tagInput.addEventListener("input", () => {
        if (tagInput.checked == true) {
            selectedModalTags.push(tagLabel.innerHTML);
        }
        else {
            selectedModalTags.splice(selectedModalTags.indexOf(tagLabel.innerHTML), 1);
        }
        selectedModalTagsInput.value = selectedModalTags;
        console.log(selectedModalTagsInput.value)///
    });
}

