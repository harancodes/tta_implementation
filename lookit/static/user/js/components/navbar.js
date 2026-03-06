// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const nav = document.querySelector('nav');

if (mobileMenuBtn && mobileMenu) {
    // Toggle menu on button click
    mobileMenuBtn.addEventListener('click', function () {
        mobileMenu.classList.toggle('active');
        // Change icon when menu is open
        if (mobileMenu.classList.contains('active')) {
            mobileMenuBtn.textContent = '✕';
        } else {
            mobileMenuBtn.textContent = '☰';
        }
    });

    // Close menu when clicking on a link
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function () {
            mobileMenu.classList.remove('active');
            mobileMenuBtn.textContent = '☰';
        });
    });

    // Close menu when clicking outside
    if (nav) {
        document.addEventListener('click', function (event) {
            if (!nav.contains(event.target) && mobileMenu.classList.contains('active')) {
                mobileMenu.classList.remove('active');
                mobileMenuBtn.textContent = '☰';
            }
        });
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const profileBtn = document.getElementById('profileDropdownBtn');
    const dropdown = document.getElementById('profileDropdownMenu');

    if (!profileBtn || !dropdown) return;

    // Toggle dropdown on click
    profileBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        const isActive = dropdown.classList.toggle('active');
        profileBtn.setAttribute('aria-expanded', isActive);
    });

    // Close when clicking outside
    document.addEventListener('click', function () {
        dropdown.classList.remove('active');
        profileBtn.setAttribute('aria-expanded', 'false');
    });

    // Prevent closing when clicking inside dropdown
    dropdown.addEventListener('click', function (e) {
        e.stopPropagation();
    });
});
