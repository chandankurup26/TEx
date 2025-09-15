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
