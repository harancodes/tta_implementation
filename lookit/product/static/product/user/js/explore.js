// Mobile Filter Toggle
const filterToggleBtn = document.getElementById('filterToggleBtn');
const mobileFilterSidebar = document.getElementById('mobileFilterSidebar');

if (filterToggleBtn && mobileFilterSidebar) {
    filterToggleBtn.addEventListener('click', function () {
        mobileFilterSidebar.classList.toggle('expanded');
        filterToggleBtn.classList.toggle('active');
    });
}

// Price Range Slider (Dual Handle) - Desktop
const priceRangeMin = document.getElementById('priceRangeMin');
const priceRangeMax = document.getElementById('priceRangeMax');
const priceRangeActive = document.getElementById('priceRangeActive');
const priceRangeWrapper = document.querySelector('.filter-sidebar:not(#mobileFilterSidebar) .price-range-wrapper');

// Price Range Slider (Dual Handle) - Mobile
const priceRangeMinMobile = document.getElementById('priceRangeMinMobile');
const priceRangeMaxMobile = document.getElementById('priceRangeMaxMobile');
const priceRangeActiveMobile = document.getElementById('priceRangeActiveMobile');
const priceRangeWrapperMobile = document.querySelector('#mobileFilterSidebar .price-range-wrapper');

function updatePriceDisplay(isMobile = false) {
    const minSlider = isMobile ? priceRangeMinMobile : priceRangeMin;
    const maxSlider = isMobile ? priceRangeMaxMobile : priceRangeMax;
    const activeLine = isMobile ? priceRangeActiveMobile : priceRangeActive;
    const wrapper = isMobile ? priceRangeWrapperMobile : priceRangeWrapper;
    const minDisplay = isMobile ? document.getElementById('priceMinDisplayMobile') : document.getElementById('priceMinDisplay');
    const maxDisplay = isMobile ? document.getElementById('priceMaxDisplayMobile') : document.getElementById('priceMaxDisplay');

    if (!minSlider || !maxSlider) return;

    const minValue = parseInt(minSlider.value);
    const maxValue = parseInt(maxSlider.value);
    const maxRange = parseInt(minSlider.max);

    // Ensure min doesn't exceed max
    if (minValue > maxValue) {
        minSlider.value = maxValue;
    }

    // Ensure max doesn't go below min
    if (maxValue < minValue) {
        maxSlider.value = minValue;
    }

    const finalMin = parseInt(minSlider.value);
    const finalMax = parseInt(maxSlider.value);

    if (minDisplay && maxDisplay) {
        minDisplay.textContent = `₹${finalMin.toLocaleString('en-IN')}`;
        maxDisplay.textContent = `₹${finalMax.toLocaleString('en-IN')}`;
    }

    // Update the colored active range line
    if (activeLine && wrapper) {
        const wrapperWidth = wrapper.offsetWidth;
        const minPercent = (finalMin / maxRange) * 100;
        const maxPercent = (finalMax / maxRange) * 100;

        activeLine.style.left = minPercent + '%';
        activeLine.style.width = (maxPercent - minPercent) + '%';
    }
}

// Desktop price range
if (priceRangeMin && priceRangeMax) {
    priceRangeMin.addEventListener('input', () => updatePriceDisplay(false));
    priceRangeMax.addEventListener('input', () => updatePriceDisplay(false));
}

// Mobile price range
if (priceRangeMinMobile && priceRangeMaxMobile) {
    priceRangeMinMobile.addEventListener('input', () => updatePriceDisplay(true));
    priceRangeMaxMobile.addEventListener('input', () => updatePriceDisplay(true));
}

// Initialize price display for both
updatePriceDisplay(false);
updatePriceDisplay(true);

// Update on window resize
window.addEventListener('resize', () => {
    updatePriceDisplay(false);
    updatePriceDisplay(true);
});

// Searchable Dropdown Functionality
function initSearchableDropdown(dropdownId, inputId, valueId, searchId) {
    const dropdown = document.getElementById(dropdownId);
    const input = document.getElementById(inputId);
    const hiddenInput = document.getElementById(valueId);
    const searchInput = document.getElementById(searchId);
    const options = dropdown.querySelectorAll('.searchable-dropdown-option');

    if (!dropdown || !input || !hiddenInput || !searchInput) return;

    // Toggle dropdown
    input.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.classList.toggle('open');
        if (dropdown.classList.contains('open')) {
            searchInput.focus();
        }
    });

    // Search functionality
    searchInput.addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        options.forEach(option => {
            const text = option.getAttribute('data-text').toLowerCase();
            if (text.includes(searchTerm)) {
                option.classList.remove('hidden');
            } else {
                option.classList.add('hidden');
            }
        });
    });

    // Select option
    options.forEach(option => {
        option.addEventListener('click', function () {
            const value = this.getAttribute('data-value');
            const text = this.getAttribute('data-text');

            input.value = text;
            hiddenInput.value = value;

            // Update selected state
            options.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            // Close dropdown
            dropdown.classList.remove('open');
            searchInput.value = '';

            // Reset hidden options
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


/*
---SEARCH SECTION---
*/
// Initialize searchable dropdowns
initSearchableDropdown('stylesDropdown', 'stylesInput', 'stylesValue', 'stylesSearch');
initSearchableDropdown('stylesDropdownMobile', 'stylesInputMobile', 'stylesValueMobile', 'stylesSearchMobile');


// Function to show and hide the clear button in search bar
const searchInput = document.getElementById('searchInput');
const searchClearBtn = document.getElementById('searchClearBtn');

if (searchInput && searchClearBtn) {
    // Show/hide clear button based on input value
    searchInput.addEventListener('input', function () {
        if (this.value.trim().length > 0) {
            searchClearBtn.classList.add('visible');
        } else {
            searchClearBtn.classList.remove('visible');
        }
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value
        || document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
}

function toggleWishlist(event, button) {
    event.preventDefault();   // stop <a> navigation
    event.stopPropagation();  // stop bubbling to parent

    const productId = button.dataset.productId;
    //wishlist count badge in navbar
    const wishlistCount = document.getElementById('wishlistCount')
    let count = Number(wishlistCount.innerText)
    console.log(count)

    fetch(toggle_wishlist_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Request failed');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'added') {
            button.classList.add('active');
            wishlistCount.innerText = count + 1
        } else if (data.status === 'removed') {
            button.classList.remove('active');
            wishlistCount.innerText = count - 1
        } else if(data.status == 'failed'){
            console.log("something went wrong")
        }
    })
    .catch(error => {
        console.error(error);
        // optional: show toast
    });
}






