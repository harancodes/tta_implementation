// // Image change functionality
let currentImageIndex = 0;
let current_url = null
let extra_image_count = 0

function changeImage(index, url) {
    currentImageIndex = parseInt(index);
    const mainImage = document.getElementById('mainImage');
    mainImage.src = url;
    current_url = url; //for setting modal image when zoom

    // Update active thumbnail
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumb, i) => {
        if (i === parseInt(index)) {
            thumb.classList.add('active');
        } else {
            thumb.classList.remove('active');
        }
    });

    // Update modal image if modal is open
    const modal = document.getElementById('imageModal');
    if (modal && modal.classList.contains('active')) {
        updateModalImage();
    }
}

// Modal functionality
function openImageModal(image_count) {
    //for disable modal button on dead end's
    extra_image_count = parseInt(image_count)

    const modal = document.getElementById('imageModal');
    modal.classList.add('active');
    updateModalImage();
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.remove('active');
    document.body.style.overflow = ''; // Restore scrolling
}

function closeImageModalOnBackdrop(event) {
    // Close modal if clicking on the backdrop (not on the image or its children)
    if (event.target.id === 'imageModal') {
        closeImageModal();
    }
}

// Prevent modal from closing when clicking on the image
document.addEventListener('DOMContentLoaded', function () {
    const modalImage = document.getElementById('modalImage');
    if (modalImage) {
        modalImage.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    }
});

//function to make modal change buttons disabled on deadend
function updateModalButtons() {
    console.log(Math.abs(currentImageIndex) , extra_image_count)
    if (Math.abs(currentImageIndex) == extra_image_count) {
        if (currentImageIndex == extra_image_count) {
            let btn1 = document.getElementById("modalNext");
            btn1.disabled = true;  // disable
        }
        if (-currentImageIndex == extra_image_count) {
            let btn2 = document.getElementById("modalPrevious");
            btn2.disabled = true;  // disable
        }
    } else {
        let btn1 = document.getElementById("modalNext");
        btn1.disabled = false;  // enable
        let btn2 = document.getElementById("modalPrevious");
        btn2.disabled = false;  // enable
    }
}

function updateModalImage() {
    const modalImageContent = document.getElementById('modalImageContent');
    updateModalButtons()
    if (modalImageContent) {
        //update modal image only if current image is changed from default
        if (current_url != null) {
            modalImageContent.src = current_url;
        }
    }
}

function changeModalImage(direction) {
    currentImageIndex += direction;
    updateModalButtons()

    id = 'imageIndex' + Math.abs(currentImageIndex)
    thumbnail_img = document.getElementById(id)
    if (thumbnail_img) {
        img_url = thumbnail_img.src

        // Update main image and thumbnails
        changeImage(currentImageIndex, img_url);
    } else {
        //reverse current image index
        currentImageIndex -= direction;
        console.log('dead-end')
    }

}

// Keyboard navigation for modal
document.addEventListener('keydown', function (event) {
    const modal = document.getElementById('imageModal');
    if (modal && modal.classList.contains('active')) {
        if (event.key === 'Escape') {
            closeImageModal();
        } else if (event.key === 'ArrowLeft') {
            changeModalImage(-1);
        } else if (event.key === 'ArrowRight') {
            changeModalImage(1);
        }
    }
});


// Like functionality
function toggleLike(button) {
    const likeCount = button.querySelector('.like-count');
    const isLiked = button.classList.contains('liked');

    if (isLiked) {
        button.classList.remove('liked');
        const currentCount = parseInt(likeCount.textContent);
        likeCount.textContent = currentCount - 1;
    } else {
        button.classList.add('liked');
        const currentCount = parseInt(likeCount.textContent);
        likeCount.textContent = currentCount + 1;
    }
}

//increase quantity display and update hidden form inupt
function increaseQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    const quantityInputForForm = document.getElementById('hiddenQuantityInput')
    const quantityInputForFormMobile = document.getElementById('hiddenQuantityInputMobile')

    let currentValue = parseInt(quantityInput.value);
    if (currentValue < 4) {
        let new_quantity = currentValue + 1;
        quantityInput.value = new_quantity
        quantityInputForForm.value = new_quantity
        if(quantityInputForFormMobile){
            quantityInputForFormMobile.value = new_quantity
        }
        console.log(new_quantity)
        console.log(quantityInput.value)
    }
}

//decrease quantity display and update hidden form inupt
function decreaseQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    const quantityInputForForm = document.getElementById('hiddenQuantityInput')
    const quantityInputForFormMobile = document.getElementById('hiddenQuantityInputMobile')

    let currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        new_quantity = currentValue - 1;
        quantityInput.value = new_quantity
        quantityInputForForm.value = new_quantity
        if(quantityInputForFormMobile){
            quantityInputForFormMobile.value = new_quantity
        }
    }
}

let selected_variant_id = null
// SETTING SELECTED SIZE AND VARIANT ID
function selectSize(btn, variant_id) {
    selected_variant_id = variant_id
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    // Select all elements with the class 'user-input'
    const inputs = document.querySelectorAll('.variant_id_field');
    // Loop through each input and set the value
    inputs.forEach(input => {
        input.value = selected_variant_id;
    });
}