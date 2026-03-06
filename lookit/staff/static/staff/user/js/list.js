
/* ============================================
   FILTERS FUNCTIONALITY
   ============================================ */
// Toggle filters functionality
function toggleFilters() {
    const filtersContainer = document.getElementById('filtersContainer');
    const filterToggle = document.getElementById('filterToggle');

    filtersContainer.classList.toggle('show');
    filterToggle.classList.toggle('active');
}

// Update select color when value changes
function updateSelectColor(select) {
    if (select.value) {
        select.classList.add('has-value');
        select.style.color = '#111827';
    } else {
        select.classList.remove('has-value');
        select.style.color = '#9ca3af';
    }
}

// Reset filters functionality
function resetFilters() {
    const filterForm = document.getElementById('filterForm');
    filterForm.reset();

    // Reset select colors to placeholder color
    const selects = filterForm.querySelectorAll('.filter-select');
    selects.forEach(select => {
        updateSelectColor(select);
    });
}

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

    // Initialize select colors and add change event listeners
    const selects = document.querySelectorAll('.filter-select');
    selects.forEach(select => {
        // Set initial color
        updateSelectColor(select);

        // Update color on change
        select.addEventListener('change', () => {
            updateSelectColor(select);
        });
    });
});

/* ============================================
   SEARCH FUNCTIONALITY
   ============================================ */
const searchInput = document.getElementById('searchInput');
const clearBtn = document.getElementById('clearBtn');

// Update clear button visibility based on input value
searchInput.addEventListener('input', () => {
    if (searchInput.value.trim().length > 0) {
        clearBtn.classList.add('show');
    } else {
        clearBtn.classList.remove('show');
    }
});



