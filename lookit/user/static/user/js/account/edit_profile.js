
// Photo Upload Functionality
document.addEventListener('DOMContentLoaded', function () {
    const profileImage = document.getElementById('profileImage');
    const profileImageInput = document.getElementById('profileImageInput');
    const changePhotoBtn = document.getElementById('changePhotoBtn');
    const imageUploadOverlay = document.getElementById('imageUploadOverlay');

    // Function to handle file selection
    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Check if the file is an image
        if (!file.type.match('image.*')) {
            alert('Please select a valid image file (JPEG, PNG, etc.)');
            return;
        }

        // Check file size (max 2MB)
        if (file.size > 2 * 1024 * 1024) {
            alert('Image size should be less than 2MB');
            return;
        }

        // Create a FileReader to read the image file
        const reader = new FileReader();

        reader.onload = function (e) {
            // Set the source of the profile image to the selected file
            profileImage.src = e.target.result;

            // Here you would typically upload the image to your server
            // For example:
            // uploadImageToServer(file);
        };

        // Read the image file as a data URL
        reader.readAsDataURL(file);
    }

    // Click event for the change photo button
    if (changePhotoBtn) {
        changePhotoBtn.addEventListener('click', function () {
            profileImageInput.click();
        });
    }

    // Click event for the image container (for the overlay)
    if (imageUploadOverlay) {
        imageUploadOverlay.addEventListener('click', function () {
            profileImageInput.click();
        });
    }

    // Change event for the file input
    if (profileImageInput) {
        profileImageInput.addEventListener('change', handleFileSelect);
    }
});

// Copy referral code functionality
const copyBtn = document.querySelector('.action-icon-btn[title="Copy"]');
if (copyBtn) {
    copyBtn.addEventListener('click', function () {
        const referralCode = document.querySelector('.referral-code').textContent;
        navigator.clipboard.writeText(referralCode).then(function () {
            // Visual feedback
            const originalSvg = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>';
            setTimeout(function () {
                copyBtn.innerHTML = originalSvg;
            }, 2000);
        });
    });
}



// Password Change Modal Functionality
document.addEventListener('DOMContentLoaded', function () {
    // Modal elements
    const modal = document.getElementById('passwordModal');
    const openModalBtn = document.querySelector('.change-password-btn');
    const closeModalBtns = document.querySelectorAll('.close-modal, .modal-overlay');
    const form = document.getElementById('changePasswordForm');
    const newPasswordInput = document.getElementById('newPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const passwordMatch = document.getElementById('passwordMatch');
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');

    // Toggle password visibility
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    });


    // Event listeners
    if (openModalBtn) {
        openModalBtn.addEventListener('click', function (e) {
            // e.preventDefault();
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (e.target === this || e.target.classList.contains('close-modal')) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
                form.reset();
                passwordMatch.textContent = '';
                passwordMatch.className = 'password-match';

                // Reset password visibility
                document.querySelectorAll('.toggle-password i').forEach(icon => {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                });
                document.querySelectorAll('.password-input input').forEach(input => {
                    input.type = 'password';
                });
            }
        });
    });

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
            form.reset();
            passwordMatch.textContent = '';
            passwordMatch.className = 'password-match';
        }
    });


});


// Email Change Modal Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Email change modal elements
    const changeEmailBtn = document.getElementById('changeEmailBtn');
    const emailModal = document.getElementById('emailChangeModal');
    const closeEmailModal = document.querySelectorAll('.close-email-modal');
    const emailChangeForm = document.getElementById('emailChangeForm');
    const newEmailInput = document.getElementById('newEmail');
    const sendLinkBtn = document.getElementById('sendLinkBtn');
    const emailSpinner = document.getElementById('emailSpinner');

    // Show email change modal
    if (changeEmailBtn) {
        changeEmailBtn.addEventListener('click', function(e) {
            // e.preventDefault();
            if (emailModal) {
                emailModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
                if (newEmailInput) newEmailInput.focus();
            }
        });
    }
//here
    // Close email change modal
    if (closeEmailModal.length > 0) {
        closeEmailModal.forEach(btn => {
            btn.addEventListener('click', function(e) {
                // e.preventDefault();
                if (emailModal) {
                    emailModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                    if (emailSpinner) emailSpinner.style.display = 'none';
                    if (emailChangeForm) emailChangeForm.reset();
                }
            });
        });
    }

    // Close modal when clicking outside
    if (emailModal) {
        emailModal.addEventListener('click', function(e) {
            if (e.target === emailModal) {
                emailModal.style.display = 'none';
                document.body.style.overflow = 'auto';
                if (emailChangeForm) emailChangeForm.reset();
            }
        });
    }

    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && emailModal && emailModal.style.display === 'flex') {
            emailModal.style.display = 'none';
            document.body.style.overflow = 'auto';
            if (emailChangeForm) emailChangeForm.reset();
        }
    });

    // Handle email change form submission
    if (emailChangeForm) {
        emailChangeForm.addEventListener('submit', function(e) {
            // e.preventDefault();
            const newEmail = newEmailInput ? newEmailInput.value.trim() : '';
            
            if (newEmail) {
                // Show loading state
                if (sendLinkBtn) sendLinkBtn.disabled = true;
                if (emailSpinner) emailSpinner.style.display = 'inline-block';
            }
        });
    }
});

// Email change modal elements
const changeEmailBtn = document.getElementById('changeEmailBtn');
const emailModal = document.getElementById('emailChangeModal');
const closeEmailModal = document.querySelectorAll('.close-email-modal');
const emailChangeForm = document.getElementById('emailChangeForm');
const newEmailInput = document.getElementById('newEmail');
const sendLinkBtn = document.getElementById('sendLinkBtn');
const emailSpinner = document.getElementById('emailSpinner');

// Function to show email modal
function showEmailModal() {
    if (emailModal) {
        emailModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        newEmailInput.focus();
    }
}

// Function to hide email modal
function hideEmailModal() {
    if (emailModal) {
        emailModal.classList.add('hidden');
        document.body.style.overflow = 'auto';
        if (emailChangeForm) emailChangeForm.reset();
    }
}

// Show email change modal
if (changeEmailBtn) {
    changeEmailBtn.addEventListener('click', showEmailModal);
}

// Close email change modal when clicking close button or overlay
if (closeEmailModal.length > 0) {
    closeEmailModal.forEach(btn => {
        btn.addEventListener('click', hideEmailModal);
    });
}

// Close modal when clicking on overlay (outside the modal content)
if (emailModal) {
    emailModal.addEventListener('click', function(e) {
        if (e.target === emailModal) {
            hideEmailModal();
        }
    });
}

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && emailModal && !emailModal.classList.contains('hidden')) {
        hideEmailModal();
    }
});

// Handle email change form submission
if (emailChangeForm) {
    emailChangeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const newEmail = newEmailInput.value.trim();
        
        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // required for Django POST
                },
                body: JSON.stringify({ email: newEmail })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error_redirect_url) {
                window.location.href = data.error_redirect_url;  // manually redirect
            }else if(data.success_redirect_url){
                window.location.href = data.success_redirect_url;  // manually redirect
            }
        })
        });
}


// Helper to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// ============================================
// TOAST NOTIFICATION FUNCTIONALITY - OVERRIDE Component
// ============================================

/**
 * Show a toast notification
 * @param {HTMLElement|string} toastElement - Toast element or selector
 */
function showToast(selector) {
    const toast = document.querySelector(selector);
    console.log("call is here")
    if (!toast) return;

    toast.classList.remove("hidden");
    toast.classList.remove("hiding");

    // Auto hide after 3 sec
    setTimeout(() => {
        toast.classList.add("hiding");

        setTimeout(() => {
            toast.classList.add("hidden");
            toast.classList.remove("hiding");
        }, 300);
    }, 3000);
}


//JQUERY FORM VALIDATION
$.validator.addMethod("letterswithspaces", function (value, element) {
    return this.optional(element) || /^[A-Za-z\s]+$/.test(value);
}, "Only letters and spaces allowed");

$.validator.addMethod("notOnlySpaces", function (value, element) {
    return this.optional(element) || value.trim().length > 0;
}, "Name cannot be only spaces");

$.validator.addMethod("strongPassword", function (value) {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(value);
}, "Password must contain uppercase, lowercase, and a number");

$.validator.addMethod("phone", function (value, element) {
    return this.optional(element) || /^[0-9]{10}$/.test(value);
}, "Enter a valid 10-digit phone number");

$.validator.addMethod("notFutureDate", function (value) {
    return !value || new Date(value) <= new Date();
}, "Date of birth cannot be in the future");

$.validator.addMethod("minAge", function (value, element, min) {
    if (!value) return true;

    const dob = new Date(value);
    const today = new Date();

    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        age--;
    }

    return age >= min;
}, "You must be at least {0} years old");

$.validator.addMethod("maxAge", function (value, element, max) {
    if (!value) return true;

    const dob = new Date(value);
    const today = new Date();

    let age = today.getFullYear() - dob.getFullYear();
    return age <= max;
}, "Please enter a valid date of birth");


document.addEventListener("DOMContentLoaded", function () {
const dobInput = document.querySelector('input[name="dob"]');
if (!dobInput) return;

const today = new Date().toISOString().split("T")[0];
dobInput.setAttribute("max", today);
});


$(document).ready(function () {

    $("#edit-profile-form").validate({
        rules: {
            full_name: {
                required: true,
                letterswithspaces: true,
                notOnlySpaces:true,
                minlength: 2,
                maxlength: 50,
            },
            email: {
                required: true,
                email: true
            },
            phone: {
                phone: true
            },
            dob: {
                notFutureDate: true,
                    minAge: 5,
                    maxAge: 130,
            }
        },
        messages: {
            full_name: {
                required: "Full name is required",
                minlength: "Name must be at least 2 characters",
                maxlength: "Name can only contain max 50 characters",
                letterswithspaces: "Name can only contain letters and spaces"
            },
            email: {
                required: "Email is required",
                email: "Please enter a valid email"
            },
            phone: {
                phone: "Enter valid phone number"
            }
        },
        onkeyup: true,
        errorClass: "error",
        errorElement: "label",
        errorPlacement: function (error, element) {
            error.insertAfter(element);
        }
    });

        $("#changePasswordForm").validate({
        rules: {
            current_password: {
                required: true,
            },
            new_password: {
                required: true,
                minlength: 8,
                strongPassword: true
            },
            confirm_new_password: {
                required: true,
                equalTo: "#newPassword"
            }
        },
        messages: {
            current_password: {
                required: "Password is required",
            },
            new_password: {
                required: "Password is required",
                minlength: "Password must be at least 8 characters",
            },
            confirm_new_password: {
                required: "Password is required",
                equalTo: "Passwords do not match"
            }
        },
        onkeyup: true,
        errorClass: "error",
        errorElement: "label",
        errorPlacement: function (error, element) {
            error.insertAfter(element.closest('.password-input'));
        }
    });
})




