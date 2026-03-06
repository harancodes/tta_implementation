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


/* ------------SEARCHABLE STYLE CATEGORY DROPDOWN---------------*/

function initSearchableDropdown(dropdownId, inputId, valueId, searchId) {
    const dropdown = document.getElementById(dropdownId);
    const input = document.getElementById(inputId);
    const hiddenInput = document.getElementById(valueId);
    const searchInput = document.getElementById(searchId);
    const options = dropdown.querySelectorAll('.searchable-dropdown-option');

    if (!dropdown || !input || !hiddenInput || !searchInput) return;

    // Toggle dropdown visibility
    input.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.classList.toggle('open');
        if (dropdown.classList.contains('open')) {
            searchInput.focus();
        }
    });

    // Filter options based on search
    searchInput.addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        options.forEach(option => {
            const text = option.getAttribute('data-text').toLowerCase();
            option.classList.toggle('hidden', !text.includes(searchTerm));
        });
    });

    // Select option
    options.forEach(option => {
        option.addEventListener('click', function () {
            const value = this.getAttribute('data-value');
            const text = this.getAttribute('data-text');

            input.value = text;
            hiddenInput.value = value;

            // Mark selected
            options.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            // Close dropdown
            dropdown.classList.remove('open');
            searchInput.value = '';
            options.forEach(opt => opt.classList.remove('hidden'));
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
            searchInput.value = '';
            options.forEach(opt => opt.classList.remove('hidden'));
        }
    });
}

// Initialize your component
initSearchableDropdown('stylesDropdownMobile', 'stylesInputMobile', 'stylesValueMobile', 'stylesSearchMobile');
