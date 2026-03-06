
// User dropdown toggle
function toggleUserDropdown(event) {
    event.stopPropagation();
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.toggle('show');
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('userDropdown');
    const userElement = document.getElementById('navbarUser');
    if (!userElement.contains(e.target)) {
        dropdown.classList.remove('show');
    }
});

// User dropdown functions
function viewProfile() {
    alert('View Profile');
    document.getElementById('userDropdown').classList.remove('show');
}

function openSettings() {
    alert('Open Settings');
    document.getElementById('userDropdown').classList.remove('show');
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        alert('Logging out...');
        // Add actual logout logic here
    }
    document.getElementById('userDropdown').classList.remove('show');
}