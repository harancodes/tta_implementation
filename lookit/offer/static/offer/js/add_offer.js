

// Toggle status text
const statusToggle = document.getElementById('status');
const statusText = document.getElementById('statusText');

statusToggle.addEventListener('change', function () {
    statusText.textContent = this.checked ? 'Active' : 'Inactive';
});

// ==========================================
// MOCK DATA FOR PRODUCTS
// ==========================================
// const availableProducts = [
//     { id: '1', name: 'Smartphone X Pro', image: 'https://via.placeholder.com/40', price: 999 },
//     { id: '2', name: 'Laptop Ultra Slim', image: 'https://via.placeholder.com/40', price: 1299 },
//     { id: '3', name: 'Wireless Noise Cancelling Headphones', image: 'https://via.placeholder.com/40', price: 299 },
//     { id: '4', name: 'Smart Watch Series 5', image: 'https://via.placeholder.com/40', price: 399 },
//     { id: '5', name: '4K Ultra HD Monitor', image: 'https://via.placeholder.com/40', price: 499 },
//     { id: '6', name: 'Gaming Mouse RGB', image: 'https://via.placeholder.com/40', price: 79 },
//     { id: '7', name: 'Mechanical Keyboard', image: 'https://via.placeholder.com/40', price: 149 },
//     { id: '8', name: 'USB-C Hub Multiport', image: 'https://via.placeholder.com/40', price: 59 },
// ];

let selectedProductIds = new Set();

// Elements
const searchBox = document.getElementById('searchBox');
const dropdownOptions = document.getElementById('dropdownOptions');
const productSearchInput = document.getElementById('productSearchInput');
const selectedPreview = document.getElementById('selectedPreview');

// Render Dropdown Options
function renderDropdownOptions(products) {
    dropdownOptions.innerHTML = '';
    if (products.length === 0) {
        dropdownOptions.innerHTML = '<div style="padding:10px; color:#666; text-align:center;">No products found</div>';
        return;
    }

    products.forEach(product => {
        const div = document.createElement('div');
        div.className = `option-item ${selectedProductIds.has(product.id) ? 'selected' : ''}`;
        // Usage of stopPropagation to prevent dropdown close
        div.onclick = (e) => {
            e.stopPropagation();
            toggleProductSelection(product.id);
        };

        div.innerHTML = `
                    <img src="${product.image_url}" alt="${product.name}" class="product-img">
                    <div class="product-info">
                        <span class="product-name">${product.name}</span>
                        <span class="product-id">ID: ${product.id}</span>
                    </div>
                    ${selectedProductIds.has(product.id) ? '<span style="color:#4f46e5; font-weight:bold;">✓</span>' : ''}
                `;
        dropdownOptions.appendChild(div);
    });
}

// Toggle Selection
function toggleProductSelection(productId) {
    if (selectedProductIds.has(productId)) {
        selectedProductIds.delete(productId);
    } else {
        selectedProductIds.add(productId);
    }

    // Re-render dropdown to update checkboxes/highlighting
    const searchTerm = productSearchInput.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(searchTerm) ||
        String(p.id).includes(searchTerm)
    );
    renderDropdownOptions(filtered);

    // Update the preview section
    updateSelectedPreview();

    // Keep focus used to be here, but we want to keep dropdown open which is handled by stopPropagation
    productSearchInput.focus();
}

// Update Selected Preview
function updateSelectedPreview() {
    selectedPreview.innerHTML = '';

    selectedProductIds.forEach(id => {
        const product = availableProducts.find(p => p.id === id);
        if (product) {
            const tag = document.createElement('div');
            tag.className = 'preview-item';
            tag.innerHTML = `
                        <input type="hidden" name="selected_products" value="${id}">
                        <img src="${product.image_url}" alt="${product.name}" class="preview-img">
                        <div class="preview-info">
                            <span class="preview-name">${product.name}</span>
                        </div>
                        <button type="button" class="remove-btn" onclick="removeTag('${id}', event)">×</button>
                    `;
            selectedPreview.appendChild(tag);
            document.getElementById('productEmptyError').classList.add('hidden')
        }
    });
}

// Remove Tag Callback (from preview)
window.removeTag = function (id, event) {
    id = Number(id)
    event.stopPropagation(); // Prevent affecting other elements
    selectedProductIds.delete(id);

    // Re-filter dropdown to consistent state
    const searchTerm = productSearchInput.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(searchTerm) ||
        String(p.id).includes(searchTerm)
    );
    renderDropdownOptions(filtered);

    updateSelectedPreview();
};

// Event Listeners for Search
productSearchInput.addEventListener('focus', () => {
    dropdownOptions.classList.add('show');
    const searchTerm = productSearchInput.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(searchTerm) ||
        String(p.id).includes(searchTerm)
    );
    renderDropdownOptions(filtered);
});

// Prevent dropdown click from closing it
dropdownOptions.addEventListener('click', (e) => {
    e.stopPropagation();
});

productSearchInput.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdownOptions.classList.add('show');
});

productSearchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(term) ||
        String(p.id).includes(term)
    );
    renderDropdownOptions(filtered);
    dropdownOptions.classList.add('show');
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('searchableDropdown');
    if (dropdown && !dropdown.contains(e.target)) {
        dropdownOptions.classList.remove('show');
    }
});

// ==========================================
// EXISTING LOGIC ADAPTED
// ==========================================

// Handle Scope Change
const offerScopeSelect = document.getElementById('offerScope');
const productSelectRow = document.getElementById('productSelectRow');
const categorySelectRow = document.getElementById('categorySelectRow');
const categorySelect = document.getElementById('categorySelect');

offerScopeSelect.addEventListener('change', function () {
    const scope = this.value;

    // Reset visibility
    productSelectRow.style.display = 'none';
    categorySelectRow.style.display = 'none';
    categorySelect.required = false;

    if (scope === 'product') {
        productSelectRow.style.display = 'flex';
        // Note: we can't set 'required' on a div, we handle validation on submit
    } else if (scope === 'category') {
        categorySelectRow.style.display = 'flex';
        categorySelect.required = true;
    }
});

// Set minimum end date based on start date
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');

startDateInput.addEventListener('change', function () {
    endDateInput.min = this.value;
    if (endDateInput.value && endDateInput.value < this.value) {
        endDateInput.value = this.value;
    }
});

// Set default start date to today
const today = new Date().toISOString().split('T')[0];
startDateInput.min = today;
startDateInput.value = today;

// ==========================================
// 🔹 JQUERY VALIDATION 
// ==========================================
$(document).ready(function () {

    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const todayStr = `${yyyy}-${mm}-${dd}`;

    $('#startDate').attr('min', todayStr);
    $('#endDate').attr('min', todayStr);

    // ==========================================
    // 🔹 CUSTOM VALIDATION RULES
    // ==========================================

    // End date must be after start date
    $.validator.addMethod("endDateAfterStart", function (value, element) {
        const start = $('#startDate').val();
        if (!start || !value) return true;
        return new Date(value) >= new Date(start);
    }, "End date must be after start date");

    // Discount limit
    $.validator.addMethod("percentageLimit", function (value, element) {
        return parseFloat(value) <= 90;
    }, "Discount percentage cannot exceed 90%");

    // Require product(s) if product scope is selected
    $.validator.addMethod("requireProducts", function (value, element) {
        const scope = $('#offerScope').val();
        if (scope === 'product') {
            return selectedProductIds && selectedProductIds.size > 0;
        }
        return true;
    }, "Please select at least one product.");

    // Require category if category scope is selected
    $.validator.addMethod("requireCategory", function (value, element) {
        const scope = $('#offerScope').val();
        if (scope === 'category') {
            return value && value.trim() !== "";
        }
        return true;
    }, "Please select a category.");

    $.validator.addMethod("requireProducts", function () {
        const scope = $('#offerScope').val();
        if (scope === 'product') {
            return selectedProductIds.size > 0;
        }
        return true;
    }, "Please select at least one product.");

    // ==========================================
    // 🔹 INITIALIZE VALIDATION
    // ==========================================
    $("#offerForm").validate({
        rules: {
            name: {
                required: true,
                minlength: 3,
                maxlength: 100
            },
            scope: {
                required: true
            },
            discount: {
                required: true,
                number: true,
                min: 1,
                percentageLimit: true
            },
            start_date: {
                required: true,
                date: true
            },
            end_date: {
                required: true,
                date: true,
                endDateAfterStart: true
            },
            style: {
                requireCategory: true
            },

        },

        messages: {
            name: {
                required: "Please enter an offer title",
                minlength: "At least 3 characters required",
                maxlength: "Maximum 100 characters allowed"
            },
            scope: {
                required: "Please select a scope"
            },
            discount: {
                required: "Enter discount percentage",
                number: "Enter a valid number",
                min: "Discount must be greater than 0",
                percentageLimit: "Discount cannot exceed 90%"
            },
            start_date: {
                required: "Start date is required"
            },
            end_date: {
                required: "End date is required",
                endDateAfterStart: "End date must be after start date"
            },
            style: {
                requireCategory: "Please select a category"
            }
        },

        errorClass: "error",
        errorElement: "label",
        errorPlacement: function (error, element) {
            error.insertAfter(element);
        },
        highlight: function (element) {
            $(element).addClass("is-invalid");
        },
        unhighlight: function (element) {
            $(element).removeClass("is-invalid");
        },

        submitHandler: function (form) {
            const scope = $('#offerScope').val();

            // Extra client-side validation
            if (scope === 'product' && (!selectedProductIds || selectedProductIds.size === 0)) {
                document.getElementById('productEmptyError').classList.remove('hidden')
                return false;
            }else{
                document.getElementById('productEmptyError').classList.add('hidden')
            }

            form.submit();
        }
    });
});



//SELECT 2 SCRIPT
// Initialize Select2 for type field
$(document).ready(function () {
    $('#categorySelect').select2({
        placeholder: 'Select Type',
        allowClear: false,
        width: '100%',
        minimumResultsForSearch: 0,
        dropdownAutoWidth: false
    });

    // Make search input appear inside the field
    $('#categorySelect').on('select2:open', function () {
        $('.select2-search__field').attr('placeholder', 'Type to search...');
    });

    // Update Select2 styling when value changes
    $('#categorySelect').on('select2:select', function () {
        $(this).next('.select2-container').find('.select2-selection__rendered').css('color', '#1f2937');
    });

    // Set initial styling for Select2
    if ($('#categorySelect').val() === '' || $('#categorySelect').val() === null) {
        $('#categorySelect').next('.select2-container').find('.select2-selection__rendered').css('color', '#9ca3af');
    }
});