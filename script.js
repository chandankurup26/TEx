const BACKEND_URL = "https://tex-wetp.onrender.com";

function toggleDarkMode() {
    const body = document.body;
    const button = document.getElementById('modeToggle');

    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        button.textContent = "Light Mode ☀️";
        localStorage.setItem('theme', 'dark');
    } else {
        button.textContent = "Dark Mode 🌑";
        localStorage.setItem('theme', 'light');
    }
}

window.onload = function () {
    const theme = localStorage.getItem('theme');
    const body = document.body;
    const button = document.getElementById('modeToggle');

    if (theme === 'dark') {
        body.classList.add('dark-mode');
        button.textContent = "Light Mode ☀️";
    } else {
        button.textContent = "Dark Mode 🌑";
    }
}

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

function processLink(event) {
    event.preventDefault();  // Prevent form submission

    const link = document.getElementById("website").value;
    const outputLabel = document.getElementById("outputLabel");
    const spinner = document.getElementById("spinner");

    if (!link) {
        showInlineMessage("Please enter a link");
        return;
    }

    outputLabel.textContent = "";      // Clear previous output
    spinner.style.display = "block";   // Show spinner

    fetch(`${BACKEND_URL}/responses`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ link })
    })
    .then(response => response.json())
    .then(data => {
        if (data.output) {
            outputLabel.textContent = data.output;
        } else {
            outputLabel.textContent = "Error: " + (data.error || "Unknown error");
        }
    })
    .catch(err => {
        console.error("Error:", err);
        showInlineMessage("Request failed");
    })
    .finally(() => {
        spinner.style.display = "none";  // Hide spinner when done
    });
}
