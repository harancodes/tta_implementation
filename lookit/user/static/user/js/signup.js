
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


$(document).ready(function () {

    $("#signup_form").validate({
        rules: {
            full_name: {
                required: true,
                letterswithspaces: true,
                notOnlySpaces: true,
                minlength: 2,
                maxlength: 50,
            },
            email: {
                required: true,
                email: true
            },
            referral_code: {
                maxlength: 50
            },
            password: {
                required: true,
                minlength: 8,
                strongPassword: true
            },
            confirm_password: {
                required: true,
                equalTo: "#password"
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
            referral_code: {
                maxlength: "Referral code cannot exceed 50 characters"
            },
            password: {
                required: "Password is required",
                minlength: "Password must be at least 8 characters"
            },
            confirm_password: {
                required: "Please confirm your password",
                equalTo: "Passwords do not match"
            }
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


//   <!--autohide server error messages after 7 seconds-->
    setTimeout(function () {
      const alerts = document.querySelectorAll('.error-box');
      alerts.forEach(alert => {
        alert.style.transition = "opacity 0.8s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 800);
      });
    }, 7000);


//  PASSWORD TOGGLE FUNCTIONLITY
    document.addEventListener('DOMContentLoaded', function() {
      // Password field toggle
      const passwordInput = document.getElementById('password');
      const passwordToggle = document.getElementById('passwordToggle');
      const eyeIcon = document.getElementById('eyeIcon');
      const eyeOffIcon = document.getElementById('eyeOffIcon');

      if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function() {
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

      // Confirm password field toggle
      const confirmPasswordInput = document.getElementById('confirm_password');
      const confirmPasswordToggle = document.getElementById('confirmPasswordToggle');
      const confirmEyeIcon = document.getElementById('confirmEyeIcon');
      const confirmEyeOffIcon = document.getElementById('confirmEyeOffIcon');

      if (confirmPasswordToggle && confirmPasswordInput) {
        confirmPasswordToggle.addEventListener('click', function() {
          const isPassword = confirmPasswordInput.type === 'password';
          
          if (isPassword) {
            confirmPasswordInput.type = 'text';
            confirmEyeIcon.style.display = 'none';
            confirmEyeOffIcon.style.display = 'block';
          } else {
            confirmPasswordInput.type = 'password';
            confirmEyeIcon.style.display = 'block';
            confirmEyeOffIcon.style.display = 'none';
          }
        });
      }
    });
