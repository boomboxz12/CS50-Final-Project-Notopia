// Get the DOMs
const username = document.getElementById("username");
const password = document.getElementById("password");
const confirmation = document.getElementById("confirmation");
const submit = document.getElementById("submit");

// Strings for later use
const passwordRules = "The password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number."
const usernameRules = "The username must only consist of alphanumeric characters."

// Array for enabling the signup button upon passing all verifications
var verifications = [0, 0, 0];

// Regular expression for password
var passRegex = /^((?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,})$/

// Regular expression for username
var userRegex = /^[a-zA-Z0-9_]*$/gm

// Inform the user about the username rules when they focus on the username field
username.addEventListener('focusin', () => {
    if (username.value == "") {
        document.getElementById("username_warning").innerHTML = usernameRules;
    }
});

// Warn the user if the username doesn't match the rules (invalid username) upon unfocusing the input field
username.addEventListener('focusout', () => {
    if (!username.value.match(userRegex)) {
        document.getElementById("username_warning").innerHTML = usernameRules;
        verifications[0] = 0;
    }
});

// Verify the validity of the username according to the rules upon releasing a key
username.addEventListener('keyup', () => {
    // If the username matches
    if (username.value.match(userRegex)) {
        // Remove error message
        document.getElementById("username_warning").innerHTML = " ";
        verifications[0] = 1;
    }
    else
    {
        verifications[0] = 0;
    }
});

// Inform the user about the password rules when they focus on the password field
password.addEventListener('focusin', () => {
    if (password.value == "") {
        document.getElementById("password_rules").innerHTML = passwordRules;
    }
});

// Warn the user if the password doesn't match the rules (invalid password) upon unfocusing the input field
password.addEventListener('focusout', () => {
    if (!password.value.match(passRegex)) {
        document.getElementById("password_rules").innerHTML = passwordRules;
        verifications[1] = 0;
    }
});

// Verify the validity of the password according to the rules upon releasing a key
password.addEventListener('keyup', () => {
    // If the password matches
    if (password.value.match(passRegex)) {
        // Remove error message
        document.getElementById("password_rules").innerHTML = " ";
        verifications[1] = 1;
    }
    else
    {
        verifications[1] = 0;
    }
});

// Warn the user that the password and confirmation don't match when the user leaves the password field
password.addEventListener('focusout', () => {
    if (confirmation.value != password.value && confirmation.value != "") {
        document.getElementById("confirmation_warning").innerHTML = "The passwords don't match.";
        verifications[2] = 0;
    }
});

// Verify that the password and confirmation match when the user leaves the password field
password.addEventListener('keyup', () => {
    if (confirmation.value == password.value) {
        document.getElementById("confirmation_warning").innerHTML = " ";
        verifications[2] = 1;
    }
    else
    {
        verifications[2] = 0;
    }
});

// Warn the user that the password and confirmation don't match when the user leaves the confirmation field
confirmation.addEventListener('focusout', () => {
    if (confirmation.value != password.value && password.value != "") {
        document.getElementById("confirmation_warning").innerHTML = "The passwords don't match.";
        verifications[2] = 0;
    }
});

// Verify that the password and confirmation match when the user leaves the confirmation field
confirmation.addEventListener('keyup', () => {
    if (confirmation.value == password.value) {
        document.getElementById("confirmation_warning").innerHTML = " ";
        verifications[2] = 1;
    }
    else
    {
        verifications[2] = 0;
    }
});

// Interval every 10ms for checking if all verifications passed
setInterval(() => {
    // If all 3 verifications pass, enable the signup button
    if (verifications.toString() == "1,1,1") {
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
