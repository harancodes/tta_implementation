/* ============================================
      INITIALIZE UI ON PAGE LOAD
      ============================================ */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize clear button visibility based on search input value
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearBtn');
    if (searchInput && clearBtn) {
        // Show/hide clear button based on input value
        if (searchInput.value.trim().length > 0) {
            clearBtn.classList.add('show');
        } else {
            clearBtn.classList.remove('show');
        }
    }

});

/* ============================================
   SEARCH FUNCTIONALITY
   ============================================ */
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const clearBtn = document.getElementById('clearBtn');

// Update clear button visibility based on input value
searchInput.addEventListener('input', () => {
    if (searchInput.value.trim().length > 0) {
        clearBtn.classList.add('show');
    } else {
        clearBtn.classList.remove('show');
    }
});

// Clear search function - just clears the input field
function clearSearch() {
    searchInput.value = '';
    clearBtn.classList.remove('show');
    searchInput.focus();
}

// Escape key to clear search
searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && searchInput.value.trim().length > 0) {
        clearSearch();
    }
});

// Action functions
function addNewStyle() {
    openAddCategoryModal();
}

function editStyle(styleId) {
    // open modal without pre-filled name
    openEditCategoryModal(styleId, '');
}

// Modal functionality
let currentStyleId = null;
let currentStyleName = null;

// Add Category Modal Functions
function openAddCategoryModal() {
    const modal = document.getElementById('addCategoryModal');
    modal.classList.add('show');
}

function closeAddCategoryModal() {
    const modal = document.getElementById('addCategoryModal');
    modal.classList.remove('show');
}


// Edit Category Modal Functions
function openEditCategoryModal(styleId) {
    const modal = document.getElementById('editCategoryModal'+styleId);
    modal.classList.add('show');
}

function closeEditCategoryModal(styleId) {
    const modal = document.getElementById('editCategoryModal'+styleId);
    modal.classList.remove('show');
    currentStyleId = null;
    currentStyleName = null;
}

// Delete Modal Functions
function openDeleteModal(styleId) {
    currentStyleId = styleId;
    const modal = document.getElementById('deleteModal' + styleId);
    modal.classList.add('show');
}

function closeDeleteModal(styleId) {
    const modal = document.getElementById('deleteModal' + styleId);
    modal.classList.remove('show');
    currentStyleId = null;
}

// Restore Modal Functions
function openRestoreModal(styleId) {
    currentStyleId = styleId;
    const modal = document.getElementById('restoreModal' + styleId);
    modal.classList.add('show');
}

function closeRestoreModal(styleId) {
    const modal = document.getElementById('restoreModal' + styleId);
    modal.classList.remove('show');
    currentStyleId = null;
}


// Close modal when clicking overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        closeAddCategoryModal();
        closeEditCategoryModal();
        closeDeleteModal();
        closeRestoreModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeAddCategoryModal();
        closeEditCategoryModal();
        closeDeleteModal();
        closeRestoreModal();
    }
});