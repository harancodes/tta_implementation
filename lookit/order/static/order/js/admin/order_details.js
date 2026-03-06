
// Modal functionality
function openStatusModal() {
  document.getElementById('statusModal').classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeStatusModal() {
  document.getElementById('statusModal').classList.remove('show');
  document.body.style.overflow = '';
}

// Close modal when clicking outside the modal content
document.getElementById('statusModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeStatusModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeStatusModal();
    }
});

// // Update the existing "Change Status" button to open the modal
// document.addEventListener('DOMContentLoaded', function() {
//     const changeStatusBtn = document.querySelector('.btn-primary i.fa-edit').closest('button');
//     if (changeStatusBtn) {
//         changeStatusBtn.onclick = openStatusModal;
//     }
// });

// Order action buttons
// document.addEventListener('DOMContentLoaded', function() {
//     // Change Order Status button
//     const changeStatusBtn = document.querySelector('.btn-primary');
//     if (changeStatusBtn) {
//         changeStatusBtn.addEventListener('click', function() {
//             console.log('Change order status clicked');
//             // Add your change status logic here
//         });
//     }
// });



    // ==============================
    // Delete Modal Functions
    // ==============================
    let currentStyleId = null;

    function openDeleteModal() {
        console.log("call is here")
        const modal = document.getElementById('deleteModal');
        if (modal) modal.classList.add('show');
    }

    function closeDeleteModal() {
        const modal = document.getElementById('deleteModal');
        if (modal) modal.classList.remove('show');
    }

    // Optional: Close modal when clicking on overlay
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-overlay')) {
            if (currentStyleId) closeDeleteModal(currentStyleId);
        }
    });

    // Optional: Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && currentStyleId) {
            closeDeleteModal(currentStyleId);
        }
    });

