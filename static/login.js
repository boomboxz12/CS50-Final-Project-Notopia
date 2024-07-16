// Get the DOMs
const username = document.getElementById("username");
const password = document.getElementById("password");
const submit = document.getElementById("submit");

// Array for enabling the log in button upon passing all verifications
var verifications = [0, 0];

// Check if a username was entered
username.addEventListener("keyup", () => {
    if (username.value.length >= 1) {
        verifications[0] = 1;
    }
    else
    {
        verifications[0] = 0;
    }
});

// Check if a password was entered
password.addEventListener("keyup", () => {
    if (password.value.length >= 1) {
        verifications[1] = 1;
    }
    else
    {
        verifications[1] = 0;
    }
});

// Interval every 10ms for checking if all verifications passed
setInterval(() => {
    // If both verifications pass, enable the log in button
    if (verifications.toString() == "1,1") {
        submit.removeAttribute("disabled");
        submit.removeAttribute("tabindex");
        submit.removeAttribute("aria-disabled");
    }
    
    // If not, disable it
    else
    {
        submit.setAttribute("disabled", "disabled");
        submit.setAttribute("tabindex", "-1");
        submit.setAttribute("aria-disabled", "true");
    }
}, 10);