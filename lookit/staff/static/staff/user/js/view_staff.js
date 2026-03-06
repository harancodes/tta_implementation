// Demote to user
function demoteToUser() {
    const modal = document.getElementById('demoteModal');
    modal.classList.add('show');
}

function closeDemoteModal() {
    const modal = document.getElementById('demoteModal');
    modal.classList.remove('show');
}

function confirmDemoteToUser() {
    alert('Staff demoted to user');
    closeDemoteModal();
    // Add actual demote logic here
}

// Block staff
function blockStaff() {
    const modal = document.getElementById('blockModal');
    modal.classList.add('show');
}

function closeBlockModal() {
    const modal = document.getElementById('blockModal');
    modal.classList.remove('show');
}

function confirmBlockStaff() {
    alert('Staff blocked');
    closeBlockModal();
    // Add actual block logic here
}

// Delete staff
function deleteStaff() {
    const modal = document.getElementById('deleteModal');
    modal.classList.add('show');
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('show');
}

function confirmDeleteStaff() {
    alert('Staff deleted');
    closeDeleteModal();
    // Add actual delete logic here
}

// Close modal when clicking overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('show');
    }
});