// Store uploaded images
let thumbnailImage = null;
// all preview additional images are stored inside here
let additionalImages = [];

// Validate thumbnail (exactly 1 required)
function validateThumbnail() {
    const validationMessage = document.getElementById('thumbnailValidationMessage');
    const uploadArea = document.getElementById('thumbnailUpload');
    const previewContainer = document.getElementById('thumbnailPreviewContainer');

    if (thumbnailImage) {
        uploadArea.classList.remove('error');
        validationMessage.classList.remove('error');
        validationMessage.classList.add('success');
        validationMessage.textContent = 'Thumbnail image uploaded successfully';
        validationMessage.style.color = '#10b981';
        previewContainer.style.display = 'block';
        return true;
    } else {
        uploadArea.classList.add('error');
        validationMessage.classList.remove('success');
        validationMessage.classList.add('error');
        validationMessage.textContent = 'Please upload exactly one thumbnail image';
        validationMessage.style.color = '#ef4444';
        previewContainer.style.display = 'none';
        return false;
    }
}

// Validate additional images (minimum 2 required)
function validateAdditionalImages() {
    const validationMessage = document.getElementById('additionalValidationMessage');
    const uploadArea = document.getElementById('additionalUpload');
    const count = additionalImages.length;

    if (count >= 2 && count <= 5) {
        uploadArea.classList.remove('error');
        validationMessage.classList.remove('error');
        validationMessage.classList.add('success');
        validationMessage.textContent = `${count} images uploaded (valid)`;
        validationMessage.style.color = '#10b981';
        return true;
    } else {
        uploadArea.classList.add('error');
        validationMessage.classList.remove('success');
        validationMessage.classList.add('error');
        validationMessage.textContent = `Please upload between 2 and 5 additional images. Currently: ${count} image${count !== 1 ? 's' : ''}`;
        validationMessage.style.color = '#ef4444';
        return false;
    }
}

// Update additional images count
function updateAdditionalImagesCount() {
    const count = additionalImages.length;
    const countElement = document.getElementById('additionalImagesCount');
    countElement.textContent = `${count} image${count !== 1 ? 's' : ''} uploaded`;
    validateAdditionalImages();
}

// Display additional images in grid
function displayAdditionalImages() {
    const grid = document.getElementById('additionalImagesGrid');
    grid.innerHTML = '';

    additionalImages.forEach((imageData, index) => {
        const imageItem = document.createElement('div');
        imageItem.className = 'image-preview-item';
        imageItem.innerHTML = `
                    <img src="${imageData.preview}" alt="Additional Image ${index + 1}">
                `;
        grid.appendChild(imageItem);
    });

    updateAdditionalImagesCount();
}

// File upload handlers
function handleThumbnailUpload(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            thumbnailImage = {
                file: file,
                preview: e.target.result,
                name: file.name
            };

            const previewImg = document.getElementById('thumbnailPreviewImg');
            previewImg.src = e.target.result;
            validateThumbnail();
        };
        reader.readAsDataURL(file);
    }
}

function handleAdditionalUpload(event) {
    const files = Array.from(event.target.files || []);

    if (files.length === 0) return;

    //replace existing additional images
    additionalImages = []

    files.forEach(file => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                additionalImages.push({
                    file: file,
                    preview: e.target.result,
                    name: file.name
                });
                displayAdditionalImages();
            };
            reader.readAsDataURL(file);
        }
    });
}

// Drag and drop functionality
const thumbnailUploadArea = document.getElementById('thumbnailUpload');
const additionalUploadArea = document.getElementById('additionalUpload');

// Thumbnail drag and drop
thumbnailUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    thumbnailUploadArea.classList.add('dragover');
});

thumbnailUploadArea.addEventListener('dragleave', () => {
    thumbnailUploadArea.classList.remove('dragover');
});

thumbnailUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    thumbnailUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        // Only take the first file for thumbnail
        const fileArray = [files[0]];
        handleThumbnailUpload({ target: { files: fileArray } });
    }
});

// Additional images drag and drop
additionalUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    additionalUploadArea.classList.add('dragover');
});

additionalUploadArea.addEventListener('dragleave', () => {
    additionalUploadArea.classList.remove('dragover');
});

additionalUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    additionalUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const fileArray = Array.from(files);
        handleAdditionalUpload({ target: { files: fileArray } });
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

// Initialize validation on page load
document.addEventListener('DOMContentLoaded', () => {
    validateThumbnail();
    validateAdditionalImages();
    updateSelectStyling();
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


//SELECT 2 SCRIPT
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
        }
    });