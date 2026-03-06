
// ==============================
// Danger Modal Functions
// ==============================

function openDangerModal() {
    const danger_modal = document.getElementById('dangerModel');
    if (danger_modal) danger_modal.classList.add('show');
}

function closeDangerModal() {
    const danger_modal = document.getElementById('dangerModel');
    if (danger_modal) danger_modal.classList.remove('show');
}

// Optional: Close danger_modal when clicking on overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('danger_modal-overlay')) {
        if (currentStyleId) closeDangerModal(currentStyleId);
    }
});

// Optional: Close danger_modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && currentStyleId) {
        closeDangerModal(currentStyleId);
    }
});

