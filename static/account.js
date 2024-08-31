document.addEventListener("DOMContentLoaded", () => {
    // Get the DOMs
    const dbPasswordInput = document.getElementById("db-password");
    const getDbButton = document.getElementById("get-db");

    // Only activate the database download button when a password is detected in the input field above it
    dbPasswordInput.addEventListener("input", () => {
        if (dbPasswordInput.value.length > 0) {
            getDbButton.removeAttribute("disabled");
            getDbButton.removeAttribute("aria-disabled");
            getDbButton.removeAttribute("tabindex");
        }
        else {
            getDbButton.setAttribute("disabled", "disabled");
            getDbButton.setAttribute("aria-disabled", "true");
            getDbButton.setAttribute("tabindex", "-1");
        }
    });
});
