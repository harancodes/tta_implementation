
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
                required: "Password is required"
            },
        },
        onkeyup: true,
        errorClass: "error",
        errorElement: "label",
        errorPlacement: function (error, element) {
            error.insertAfter(element);
        }
    });
});


// <!--autohide error messages after 4 seconds-->
setTimeout(function () {
    const alerts = document.querySelectorAll('.error-box');
    alerts.forEach(alert => {
        alert.style.transition = "opacity 0.8s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 800);
    });
}, 4000);
