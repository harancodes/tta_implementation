// Delete Modal Functions
function openDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.add('show');
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('show');
}

// Restore Modal Functions
function openRestoreModal() {
    const modal = document.getElementById('restoreModal');
    modal.classList.add('show');
}

function closeRestoreModal() {
    const modal = document.getElementById('restoreModal');
    modal.classList.remove('show');
}


// Close modal when clicking overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        closeDeleteModal();
    }
});