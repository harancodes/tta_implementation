// ============================================
// TOAST NOTIFICATION FUNCTIONALITY
// ============================================

/**
 * Show a toast notification
 * @param {HTMLElement|string} toastElement - Toast element or selector
 */
function showToast(toastElement) {
    const toast = typeof toastElement === 'string'
        ? document.querySelector(toastElement)
        : toastElement;

    if (!toast) return;

    toast.classList.remove('hidden');
    // toast.style.display = 'flex';
}

/**
 * Close a toast notification
 * @param {HTMLElement} closeButton - The close button element
 */
function closeToast(closeButton) {
    const toast = closeButton.closest('.toast');
    if (!toast) return;

    toast.classList.add('hiding');
    setTimeout(() => {
        toast.classList.add('hidden');
        toast.classList.remove('hiding');
    }, 300);
}

// Initialize: Add click handlers to all close buttons on page load
document.addEventListener('DOMContentLoaded', () => {
    const closeButtons = document.querySelectorAll('.toast-close');
    closeButtons.forEach(button => {
        if (!button.onclick) {
            button.addEventListener('click', function () {
                closeToast(this);
            });
        }
    });
});

//   <!--autohide messages after 3 seconds-->

setTimeout(function () {
    const toast = document.querySelectorAll('.toast');
    toast.forEach(alert => {
        alert.style.transition = "opacity 0.8s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 800);
    });
}, 3000);
