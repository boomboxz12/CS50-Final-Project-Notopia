// Get the DOMs
const deleteTagCheckbox = document.querySelectorAll(".delete-tag-checkbox");
const deleteTagButton = document.querySelectorAll(".delete-tag-button");

// Only activate the delete tag button when the confirmation checkbox is checked
deleteTagCheckbox.forEach(deletionCheckbox);
function deletionCheckbox(checkbox) {
    checkbox.addEventListener("input", () => {
        if (checkbox.checked) {
            deleteTagButton.forEach(deletionButton)
            function deletionButton(button) {
                if (checkbox.parentElement.parentElement == button.parentElement) {
                    button.removeAttribute("disabled");
                    button.removeAttribute("tabindex");
                    button.removeAttribute("aria-disabled");
                }
            }
        }
        else if (!checkbox.checked) {
            deleteTagButton.forEach(deletionButton)
            function deletionButton(button) {
                if (checkbox.parentElement.parentElement == button.parentElement) {
                    button.setAttribute("disabled", "");
                    button.setAttribute("tabindex", "-1");
                    button.setAttribute("aria-disabled", "true");
                }
            }
        }
    });
}
