

// Search functionality
const searchInput = document.querySelector('.search-orders input');
const clearSearchBtn = document.querySelector('.search-orders .clear-search');

// Show/hide clear button based on input
searchInput.addEventListener('input', function() {
    if (this.value.trim() !== '') {
        clearSearchBtn.style.display = 'flex';
    } else {
        clearSearchBtn.style.display = 'none';
    }
});

// Clear search input
clearSearchBtn.addEventListener('click', function() {
    searchInput.value = '';
    this.style.display = 'none';
    // Here you would typically trigger a search with empty query to show all results
    console.log('Search cleared');
});

// Handle search on enter
searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        // Here you would typically trigger a search with the input value
        console.log('Searching for:', this.value);
    }
});
