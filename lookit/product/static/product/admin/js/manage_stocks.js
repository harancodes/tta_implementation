// Helper function to properly close a dropdown
function closeDropdown(dropdown) {
    dropdown.classList.remove('show');
    dropdown.style.top = '';
    dropdown.style.right = '';
    dropdown.style.visibility = '';
    dropdown.style.display = '';
}

// Close all dropdowns
function closeAllDropdowns() {
    document.querySelectorAll('.actions-dropdown').forEach(d => {
        closeDropdown(d);
    });
}

// Toggle actions dropdown
function toggleActionsDropdown(event, variantId) {
    event.stopPropagation();
    const dropdown = document.getElementById(`actions-${variantId}`);
    const allDropdowns = document.querySelectorAll('.actions-dropdown');
    const button = event.currentTarget;

    // Close all other dropdowns
    allDropdowns.forEach(d => {
        if (d.id !== `actions-${variantId}`) {
            closeDropdown(d);
        }
    });

    // Toggle current dropdown
    const isOpen = dropdown.classList.contains('show');

    if (!isOpen) {
        // Temporarily show dropdown to measure it (hidden from view)
        dropdown.style.visibility = 'hidden';
        dropdown.style.display = 'block';
        dropdown.style.top = '-9999px';
        dropdown.style.right = '0';
        dropdown.classList.add('show');

        // Force a reflow to get accurate measurements
        void dropdown.offsetHeight;

        // Get actual dimensions
        const dropdownRect = dropdown.getBoundingClientRect();
        const dropdownHeight = dropdownRect.height;
        const dropdownWidth = dropdownRect.width;

        // Calculate button position
        const rect = button.getBoundingClientRect();
        const gap = 5;

        // Position below button by default
        let top = rect.bottom + gap;
        let right = window.innerWidth - rect.right;

        // Check if dropdown would go off bottom of screen
        if (top + dropdownHeight > window.innerHeight - gap) {
            // Position above button instead
            top = rect.top - dropdownHeight - gap;
            // If still goes off top, position at bottom of screen
            if (top < gap) {
                top = window.innerHeight - dropdownHeight - gap;
            }
        }

        // Adjust horizontal position if needed
        if (right + dropdownWidth > window.innerWidth - gap) {
            right = window.innerWidth - rect.left - dropdownWidth;
            if (right < gap) {
                right = gap;
            }
        }

        // Apply final positioning
        dropdown.style.top = `${top}px`;
        dropdown.style.right = `${right}px`;
        dropdown.style.visibility = 'visible';
    } else {
        closeDropdown(dropdown);
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    // Don't close if clicking on the dropdown itself or the button
    if (!e.target.closest('.actions-cell') && !e.target.closest('.actions-dropdown')) {
        closeAllDropdowns();
    }
});

// Close dropdowns on scroll
let scrollTimeout;
window.addEventListener('scroll', () => {
    // Clear any existing timeout
    clearTimeout(scrollTimeout);

    // Close dropdowns immediately
    closeAllDropdowns();
}, true);

// Close dropdowns on resize
let resizeTimeout;
window.addEventListener('resize', () => {
    // Debounce resize events
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        closeAllDropdowns();
    }, 100);
});

// Store original stock values
const originalStockValues = {};

// Initialize original stock values
function initializeOriginalStockValues() {
    for (let i = 1; i <= 6; i++) {
        const stockElement = document.getElementById(`stock-${i}`);
        if (stockElement) {
            originalStockValues[i] = parseInt(stockElement.textContent);
        }
    }
}

// Check if any stock values have been modified
function checkForStockChanges() {
    let hasChanges = false;
    for (let i = 1; i <= 6; i++) {
        const stockElement = document.getElementById(`stock-${i}`);
        if (stockElement) {
            const currentValue = parseInt(stockElement.textContent);
            const originalValue = originalStockValues[i];
            const stockControl = stockElement.closest('.stock-control');

            if (currentValue !== originalValue) {
                stockElement.classList.add('modified');
                if (stockControl) {
                    stockControl.classList.add('modified');
                }
                hasChanges = true;
            } else {
                stockElement.classList.remove('modified');
                if (stockControl) {
                    stockControl.classList.remove('modified');
                }
            }
        }
    }

    // Enable/disable buttons based on changes
    const resetBtn = document.getElementById('resetBtn');
    const saveBtn = document.getElementById('saveBtn');
    if (resetBtn) resetBtn.disabled = !hasChanges;
    if (saveBtn) saveBtn.disabled = !hasChanges;
}



// Reset changes
function resetChanges() {
    if (confirm('Are you sure you want to reset all stock changes? This will revert all modifications.')) {
        for (let i = 1; i <= 6; i++) {
            const stockElement = document.getElementById(`stock-${i}`);
            if (stockElement && originalStockValues[i] !== undefined) {
                stockElement.textContent = originalStockValues[i];
            }
        }
        checkForStockChanges();
    }
}

// Save changes
function saveChanges() {
    const changes = {};
    let hasChanges = false;

    for (let i = 1; i <= 6; i++) {
        const stockElement = document.getElementById(`stock-${i}`);
        if (stockElement) {
            const currentValue = parseInt(stockElement.textContent);
            const originalValue = originalStockValues[i];

            if (currentValue !== originalValue) {
                changes[i] = currentValue;
                hasChanges = true;
            }
        }
    }

    if (!hasChanges) {
        alert('No changes to save.');
        return;
    }

    // Update original values to current values
    Object.keys(changes).forEach(id => {
        originalStockValues[parseInt(id)] = changes[id];
    });

    // Reset visual indicators
    checkForStockChanges();

    // Add actual API call here to save changes
    console.log('Saving stock changes:', changes);
    alert('Stock changes saved successfully!');
}


// Edit variant
function editVariant(variantId) {
    const dropdown = document.getElementById(`actions-${variantId}`);
    closeDropdown(dropdown);
    alert(`Edit variant ${variantId}`);
    // Add navigation to edit page or open modal
}

// Format date time
function formatDateTime(date) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const month = months[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    let hours = date.getHours();
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    return `${month} ${day}, ${year} ${hours}:${minutes} ${ampm}`;
}

// Update last updated timestamp
function updateLastUpdated(variantId) {
    const lastUpdatedElement = document.getElementById(`last-updated-${variantId}`);
    if (lastUpdatedElement) {
        const now = new Date();
        lastUpdatedElement.textContent = formatDateTime(now);
    }
}

// Open remove modal
function openRemoveModal(variantId) {
    currentVariantId = variantId;
    const modal = document.getElementById('removeModal'+variantId);
    modal.classList.add('show');
}

// Close remove modal
function closeRemoveModal() {
    const modal = document.getElementById('removeModal'+currentVariantId);
    modal.classList.remove('show');
    currentVariantId = null;
}

// Confirm remove
// function confirmRemove() {
//     if (currentVariantId) {
//         const stockElement = document.getElementById(`stock-${currentVariantId}`);
//         if (stockElement) {
//             const row = stockElement.closest('tr');
//             if (row) {
//                 row.remove();
//             }
//         }
//         alert(`Variant ${currentVariantId} removed`);
//         // Add actual API call here
//     }
//     closeRemoveModal();
// }

// Open delete modal
function openDeleteModal(variantId) {
    currentVariantId = variantId;
    const dropdown = document.getElementById(`actions-${variantId}`);
    closeDropdown(dropdown);
    const modal = document.getElementById('deleteModal');
    modal.classList.add('show');
}

// Close delete modal
function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('show');
    currentVariantId = null;
}

// Confirm delete
function confirmDelete() {
    if (currentVariantId) {
        const stockElement = document.getElementById(`stock-${currentVariantId}`);
        if (stockElement) {
            const row = stockElement.closest('tr');
            if (row) {
                row.remove();
            }
        }
        alert(`Variant ${currentVariantId} deleted`);
        // Add actual API call here
    }
    closeDeleteModal();
}

// Close modal when clicking overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        closeRemoveModal();
        closeDeleteModal();
        closeAddSizeModal();
    }
});

// ============================================
// ADD NEW SIZE MODAL FUNCTIONALITY
// ============================================

// Get next available variant ID (using stock elements)
function getNextVariantId() {
    const existingIds = Array.from(document.querySelectorAll('.stock-value')).map(el => {
        const id = el.id.replace('stock-', '');
        return parseInt(id) || 0;
    });
    const maxId = existingIds.length > 0 ? Math.max(...existingIds) : 0;
    return maxId + 1;
}

// Check if size already exists
function sizeExists(size) {
    const rows = document.querySelectorAll('.variants-table tbody tr');
    for (let row of rows) {
        const sizeCell = row.querySelector('td:first-child');
        if (sizeCell && sizeCell.textContent.trim() === size) {
            return true;
        }
    }
    return false;
}

// Open add size modal
function openAddSizeModal() {
    const modal = document.getElementById('addSizeModal');
    modal.classList.add('show');
    // Reset form
    document.getElementById('newSizeSelect').value = '';
    document.getElementById('newStockAmount').value = '';
}

// Close add size modal
function closeAddSizeModal() {
    const modal = document.getElementById('addSizeModal');
    modal.classList.remove('show');
    // Reset form
    document.getElementById('newSizeSelect').value = '';
    document.getElementById('newStockAmount').value = '';
}


// Pagination functionality
function changePage(page) {
    const buttons = document.querySelectorAll('.pagination-btn');
    let targetPage = page;

    if (page === 'prev') {
        // Previous button
        const currentPage = document.querySelector('.pagination-btn.active');
        const currentIndex = Array.from(buttons).indexOf(currentPage);
        if (currentIndex > 1) {
            targetPage = parseInt(buttons[currentIndex - 1].textContent);
        } else {
            return; // Already on first page
        }
    } else if (page === 'next') {
        // Next button
        const currentPage = document.querySelector('.pagination-btn.active');
        const currentIndex = Array.from(buttons).indexOf(currentPage);
        if (currentIndex < buttons.length - 2) {
            targetPage = parseInt(buttons[currentIndex + 1].textContent);
        } else {
            return; // Already on last page
        }
    }

    // Remove active class from all buttons
    buttons.forEach(btn => btn.classList.remove('active'));

    // Add active class to target page button
    buttons.forEach((btn, index) => {
        if (parseInt(btn.textContent) === targetPage) {
            btn.classList.add('active');
        }
    });

    // Update previous/next button states
    const activeButton = document.querySelector('.pagination-btn.active');
    const activeIndex = Array.from(buttons).indexOf(activeButton);
    buttons[0].disabled = activeIndex === 1; // First page
    buttons[buttons.length - 1].disabled = activeIndex === buttons.length - 2; // Last page

    // Add actual API call here to fetch page data
    console.log(`Loading page ${targetPage}`);
}


// Update stock
function updateStock(variantId, change) {
    stock = document.getElementById(variantId).innerText
    stock = parseInt(stock) + change
    if(stock >= 0){
        document.getElementById(variantId).innerHTML = stock

        //make submit stock button active
        sumbitBtn = document.getElementById(variantId+'-submitBtn')
        sumbitBtn.disabled = false
    }
}

function submitStock(variantId, csrfToken) {
    newStock = document.getElementById(variantId).innerText

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            variant_id: variantId,
            stock: Number(newStock),
        }),
    })
        .then(response => response.json())
        .then(data => {
            sumbitBtn = document.getElementById(variantId+'-submitBtn')
            sumbitBtn.disabled = true
            document.getElementById('totalStock').innerHTML = data.new_total_stock;
        });
}
