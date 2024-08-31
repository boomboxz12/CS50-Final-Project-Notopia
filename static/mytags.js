document.addEventListener("DOMContentLoaded", () => {
    // Get the DOMs
    const deleteTagCheckbox = document.querySelectorAll(".delete-tag-checkbox");
    const deleteTagButton = document.querySelectorAll(".delete-tag-button");
    const createTagButton = document.getElementById("create-tag-button");
    const createTagInput = document.getElementById("create-tag-input")

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

    // Only activate the create tag button when the tag title field is populated
    createTagInput.addEventListener("input", () => {
        if (createTagInput.value.length > 0) {
            createTagButton.removeAttribute("disabled");
            createTagButton.removeAttribute("aria-disabled");
            createTagButton.removeAttribute("tabindex");
        }
        else {
            createTagButton.setAttribute("disabled", "disabled");
            createTagButton.setAttribute("aria-disabled", "true");
            createTagButton.setAttribute("tabindex", "-1");
        }
    });
});
