
$(document).ready(function () {

    $("#login_form").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true
            }
        },
        messages: {
            email: {
                required: "Email is required",
                email: "Please enter a valid email"
            },
            password: {
                required: "Password is required",
                minlength: "Password must be at least 8 characters"
            },
        },
        onkeyup: true,
        errorClass: "error",
        errorElement: "label",
        errorPlacement: function (error, element) {
            // For password fields wrapped in password-wrapper, insert after the wrapper
            if (element.closest('.password-wrapper').length) {
                error.insertAfter(element.closest('.password-wrapper'));
            } else {
                error.insertAfter(element);
            }
        },
        success: function (label, element) {
            // Remove error styling when field is valid
            label.remove();
        }
    });
});


//   <!--autohide error messages after 7 seconds-->
setTimeout(function () {
    const alerts = document.querySelectorAll('.error-box');
    alerts.forEach(alert => {
        alert.style.transition = "opacity 0.8s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 800);
    });
}, 7000);


//   <!-- Password Toggle Functionality -->

document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    const eyeIcon = document.getElementById('eyeIcon');
    const eyeOffIcon = document.getElementById('eyeOffIcon');

    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function () {
            const isPassword = passwordInput.type === 'password';

            if (isPassword) {
                passwordInput.type = 'text';
                eyeIcon.style.display = 'none';
                eyeOffIcon.style.display = 'block';
            } else {
                passwordInput.type = 'password';
                eyeIcon.style.display = 'block';
                eyeOffIcon.style.display = 'none';
            }
        });
    }
});
