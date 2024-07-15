// Get username, password, and confirmation DOMs
const username = document.getElementById("username");
const password = document.getElementById("password");
const confirmation = document.getElementById("confirmation");
const submit = document.getElementById("submit");

// Array for enabling the signup button upon passing all verifications
var verifications = [0, 0, 0];

// Verify that a username was entered upon unfocusing the input field
username.addEventListener("focusout", () => {
    if (username.value.length < 1) {
        // Warn the user if they leave the input field without entering a username
        document.getElementById("username_warning").innerHTML = "Please enter a username.";
        verifications[0] = 0;
    }
});

// Remove the warning when the user inputs something in the input field
username.addEventListener("keyup", () => {
    if (username.value.length >= 1) {
        document.getElementById("username_warning").innerHTML = " ";
        verifications[0] = 1;
    }
    else
    {
        verifications[0] = 0;
    }
});

// Warn the user if the password doesn't match the rules (invalid password) upon unfocusing the input field
password.addEventListener('focusout', () => {
    if (!password.value.match(/^((?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{7,})$/)) {
        document.getElementById("password_rules").innerHTML = "The password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number.";
        verifications[1] = 0;
    }
  });

// Verify the validity of the password according to the rules upon releasing a key
password.addEventListener('keyup', () => {
    // If the password matches
    if (password.value.match(/^((?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{7,})$/)) {
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
        submit.classList.remove("disabled")
    }
    
    // If not, disable it
    else
    {
        submit.classList.add("disabled")
    }
}, 10);
