const passwordInput = document.getElementById("password");
const showPasswordButton = document.getElementById("showPassword");
const loginForm = document.getElementById("loginForm");

// Show or hide the password
showPasswordButton.addEventListener("click", function () {
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        showPasswordButton.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        showPasswordButton.textContent = "Show";
    }
});


