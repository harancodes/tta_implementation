const modal = document.getElementById('addAddressModal');
const addressForm = document.getElementById('addressForm');
const closeModalBtn = document.getElementById('closeAddModel');
const cancelBtn = document.getElementById('btn-outline');

function openAddAddressModal() {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = window.innerWidth - document.documentElement.clientWidth + 'px';
}

function closeAddAddressModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    addressForm.reset();
}

// Close modal when clicking close button or cancel
closeModalBtn.addEventListener('click', closeAddAddressModal);
cancelBtn.addEventListener('click', closeAddAddressModal);

// Close modal when clicking outside the modal content
modal.addEventListener('click', function(e) {
    if (e.target === modal) {
        closeAddAddressModal();
    }
});


//Form Jquery validation
// Only letters and spaces (not only spaces)
$.validator.addMethod("lettersWithSpaces", function (value, element) {
    return this.optional(element) ||
        /^[A-Za-z][A-Za-z\s]*$/.test(value.trim());
}, "Only letters and spaces allowed");

$.validator.addMethod("notOnlySpaces", function (value, element) {
    return this.optional(element) || value.trim().length > 0;
}, "Name cannot be only spaces");


// Indian phone number (10 digits)
$.validator.addMethod("phoneIN", function (value, element) {
    return this.optional(element) || /^[6-9]\d{9}$/.test(value);
}, "Enter a valid phone number");

// PIN code (India – 6 digits)
$.validator.addMethod("pincodeIN", function (value, element) {
    return this.optional(element) || /^[1-9]\d{5}$/.test(value);
}, "Enter a valid PIN code");


$(document).ready(function () {

    $("#addressForm").validate({
        rules: {
            full_name: {
                required: true,
                lettersWithSpaces: true,
                notOnlySpaces: true,
                minlength: 2,
                maxlength: 50
            },
            phone: {
                required: true,
                phoneIN: true
            },
            second_phone: {
                phoneIN: true
            },
            address_line: {
                required: true,
                minlength: 5,
                maxlength: 255
            },
            city: {
                required: true,
                lettersWithSpaces: true
            },
            state: {
                required: true,
                lettersWithSpaces: true
            },
            pincode: {
                required: true,
                pincodeIN: true
            },
            type: {
                required: true
            }
        },

        messages: {
            full_name: {
                required: "Full name is required",
                minlength: "Name must be at least 2 characters",
                maxlength: "Name cannot exceed 50 characters",
                notOnlySpaces: "Name cannot be only spaces",
            },
            phone: {
                required: "Phone number is required"
            },
            address_line: {
                required: "Address is required",
                minlength: "Address is too short"
            },
            city: {
                required: "City is required"
            },
            state: {
                required: "State is required"
            },
            pincode: {
                required: "PIN code is required"
            },
            type: {
                required: "Please select address type"
            }
        },

        onkeyup: true,

        errorClass: "error",
        errorElement: "label",

        errorPlacement: function (error, element) {
            // Match your existing error label behavior
            if (element.closest(".input-with-icon").length) {
                error.insertAfter(element.closest(".input-with-icon"));
            } else if (element.closest(".select-wrapper").length) {
                error.insertAfter(element.closest(".select-wrapper"));
            } else {
                error.insertAfter(element);
            }
        },

        success: function (label) {
            // IMPORTANT: remove empty error labels to avoid layout gaps
            label.remove();
        }
    });

});
