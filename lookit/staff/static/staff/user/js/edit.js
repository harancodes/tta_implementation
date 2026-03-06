// Change photo
function changePhoto() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const profileImage = document.querySelector('.profile-image');
                profileImage.innerHTML = `<img src="${e.target.result}" alt="Profile">`;
            };
            reader.readAsDataURL(file);
        }
    };
    input.click();
}

// Promote as staff
function promoteAsStaff() {
    const modal = document.getElementById('promoteModal');
    modal.classList.add('show');
}

function closePromoteModal() {
    const modal = document.getElementById('promoteModal');
    modal.classList.remove('show');
}

function confirmPromoteAsStaff() {
    alert('User promoted as staff');
    closePromoteModal();
    // Add actual promotion logic here
}

// Close modal when clicking overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('show');
    }
});

// Save changes
function saveChanges() {
    const fullName = document.getElementById('fullName').value;
    const phone = document.getElementById('phone').value;
    const gender = document.getElementById('gender').value;
    const dob = document.getElementById('dob').value;

    if (!fullName || !phone || !gender || !dob) {
        alert('Please fill in all fields');
        return;
    }

    alert('Changes saved successfully');
    // Add actual save logic here
}
