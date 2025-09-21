function toggleDarkMode() {
    const body = document.body;
    const button = document.getElementById('modeToggle');

    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        button.textContent = "Light Mode ☀️"; // Light mode icon
        localStorage.setItem('theme', 'dark');
    }
    else {
        button.textContent = "Dark Mode🌙"; // Dark mode icon
        localStorage.setItem('theme', 'light');
    }
}

// On page load, apply saved theme
window.onload = function () {
    const theme = localStorage.getItem('theme');
    const button = document.getElementById('modeToggle');

    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
        button.textContent = "Light Mode ☀️";
    }
    else {
        button.textContent = "Dark Mode🌙";
    }
};

function copyText() {
    const text = document.getElementById("outputLabel").textContent;

    navigator.clipboard.writeText(text)
        .then(() => {
            showInlineMessage("Copied!");
        })
        .catch(err => {
            console.error("Failed to copy text: ", err);
            showInlineMessage("Failed to copy");
        });
}

function showInlineMessage(message) {
    const msgSpan = document.getElementById("copyMessage");
    msgSpan.textContent = message;
    msgSpan.classList.add("show");
    // Hide the message after 2 seconds
    setTimeout(() => {
        msgSpan.classList.remove("show");
    }, 2000);
}
