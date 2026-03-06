// ============================================
// MAIN CONTENT FUNCTIONALITY
// ============================================

// Store original values
let originalAdditionalImagesCount = 0;
let newAdditionalImagesCount = 0;


// Check if field value has changed
function checkFieldChange(input) {
    const fieldId = input.id || input.name;
    const currentValue = input.type === 'checkbox' ? input.checked : input.value;
    const originalValue = originalValues[fieldId];
    const formGroup = input.closest('.form-group');

    if (formGroup) {
        if (currentValue !== originalValue) {
            formGroup.classList.add('modified');
        } else {
            formGroup.classList.remove('modified');
        }
    }
}

// Track all form field changes
function setupChangeTracking() {
    const form = document.getElementById('editProductForm');
    const inputs = form.querySelectorAll('input, select, textarea');

    inputs.forEach(input => {
        if (input.type === 'file') return;

        // Track changes on input, change, and blur events
        input.addEventListener('input', () => checkFieldChange(input));
        input.addEventListener('change', () => checkFieldChange(input));
        input.addEventListener('blur', () => checkFieldChange(input));
    });
}

// Handle thumbnail image replace
function handleThumbnailReplace(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const thumbnailImage = document.getElementById('thumbnailImage');
            const thumbnailPreview = thumbnailImage.closest('.thumbnail-preview');
            const imageContainer = thumbnailPreview.closest('.image-preview-container');

            thumbnailImage.src = e.target.result;

            // Mark as modified if different from original
            if (e.target.result !== originalThumbnailSrc) {
                thumbnailPreview.classList.add('modified');
                imageContainer.classList.add('modified');
            } else {
                thumbnailPreview.classList.remove('modified');
                imageContainer.classList.remove('modified');
            }
        };
        reader.readAsDataURL(file);
        console.log('Thumbnail image replaced:', file.name);
    }
}

// Handle additional images add
function handleAdditionalImagesAdd(event) {
    const files = event.target.files;
    if (files.length > 0) {
        const grid = document.getElementById('newAdditionalImagesGrid');
        const imagesGroup = grid.closest('.form-group');

        //CLEAR PREVIOUS FILES SELECT
        grid.innerHTML = "";

        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const imageItem = document.createElement('div');
                imageItem.className = 'additional-image-item modified';
                imageItem.innerHTML = `
                            <img src="${e.target.result}" alt="Additional Image">

                        `;
                grid.appendChild(imageItem);

                // Mark images section as modified
                imagesGroup.classList.add('modified-images');
            };
            reader.readAsDataURL(file);
        });

        console.log(`${files.length} additional image(s) added`);
        newAdditionalImagesCount = files.length;
        updateAdditionalImagesModifiedState();
    }
}

// Remove additional image
function removeAdditionalImage(button) {
        const imageItem = button.closest('.additional-image-item');
        const imagesGroup = imageItem.closest('.form-group');

        // Mark as modified when removing (whether original or new image)
        imagesGroup.classList.add('modified-images');
        imageItem.remove();
        console.log('Image removed');
        updateAdditionalImagesModifiedState();
}


// Update additional images modified state
function updateAdditionalImagesModifiedState() {
    const grid = document.getElementById('additionalImagesGrid');
    const imagesGroup = grid.closest('.form-group');
    const currentCount = grid.querySelectorAll('.additional-image-item').length;

    if (currentCount !== originalAdditionalImagesCount) {
        imagesGroup.classList.add('modified-images');
    } else {
        // Check if all images are original (not modified)
        const modifiedImages = grid.querySelectorAll('.additional-image-item.modified');
        if (modifiedImages.length === 0) {
            imagesGroup.classList.remove('modified-images');
        }
    }
}

// Drag and drop functionality for additional images
const addImagesArea = document.getElementById('addImagesArea');

addImagesArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    addImagesArea.classList.add('dragover');
});

addImagesArea.addEventListener('dragleave', () => {
    addImagesArea.classList.remove('dragover');
});

addImagesArea.addEventListener('drop', (e) => {
    e.preventDefault();
    addImagesArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const fileList = new DataTransfer();
        Array.from(files).forEach(file => fileList.items.add(file));
        document.getElementById('additionalInput').files = fileList.files;
        handleAdditionalImagesAdd({ target: { files: files } });
    }
});

// Handle select styling for inactive default options
function updateSelectStyling() {
    const selects = document.querySelectorAll('select[required]:not(.select2-hidden-accessible)');
    selects.forEach(select => {
        if (select.value === '' || select.options[select.selectedIndex].disabled) {
            select.style.color = '#9ca3af';
        } else {
            select.style.color = '#1f2937';
        }
    });
}

// Add event listeners to all selects (excluding Select2)
document.querySelectorAll('select[required]:not(.select2-hidden-accessible)').forEach(select => {
    select.addEventListener('change', updateSelectStyling);
});

// Initialize Select2 for type field
$(document).ready(function () {
    $('#type').select2({
        placeholder: 'Select Type',
        allowClear: false,
        width: '100%',
        minimumResultsForSearch: 0,
        dropdownAutoWidth: false
    });

    // Make search input appear inside the field
    $('#type').on('select2:open', function () {
        $('.select2-search__field').attr('placeholder', 'Type to search...');
    });

    // Update Select2 styling when value changes
    $('#type').on('select2:select', function () {
        $(this).next('.select2-container').find('.select2-selection__rendered').css('color', '#1f2937');
    });

    // Set initial styling for Select2
    if ($('#type').val() === '' || $('#type').val() === null) {
        $('#type').next('.select2-container').find('.select2-selection__rendered').css('color', '#9ca3af');
    } else {
        $('#type').next('.select2-container').find('.select2-selection__rendered').css('color', '#1f2937');
    }
});


