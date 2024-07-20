// Get the DOMs
const noteTitle = document.getElementById("title");
const noteBody = document.getElementById("note");
const submit = document.getElementById("submit");
const form = document.getElementById("form")

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

// Using BeforeUnloadEvent to warn the user if they leave the page without saving
const titleValue = noteTitle.value;
const bodyValue = noteBody.value;
let submitted = false;
window.onbeforeunload = function() {
    if (!submitted) {
        if (noteTitle.value != titleValue || noteBody.value != bodyValue) {
            return "You have unsaved changes. Are you sure you want to leave?";
        }
}}
