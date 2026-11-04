const currentDate = document.getElementById("currentDate");
const notificationButton = document.getElementById("profileButton");
const logoutButton = document.getElementById("logoutButton");
const dashboardMessage = document.getElementById("dashboardMessage");

// Display today's date automatically
const today = new Date();

currentDate.textContent = today.toLocaleDateString("en-IN", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric"
});

// Demo profile interaction
notificationButton.addEventListener("click", function () {
    dashboardMessage.textContent =
        "Faculty profile preview. Authentication will be connected later.";
});

// Demo logout
logoutButton.addEventListener("click", function () {
    const confirmed = confirm("Return to the login page?");

    if (confirmed) {
        window.location.href = "login.html";
    }
});