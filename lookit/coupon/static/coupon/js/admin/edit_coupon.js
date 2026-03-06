$(document).ready(function () {

});
$(document).ready(function () {
    //convert coupon code to upper case
    document.getElementById("couponCode").addEventListener("input", function () {
        this.value = this.value.toUpperCase();
    });

    // Prevent spacebar input for coupon code
    document.getElementById("couponCode").addEventListener("keydown", function (e) {
        if (e.key === " ") {
            e.preventDefault();
        }
    });

    // Set today's date as min selectable date for start_date and end_date
    // const today = new Date();
    // const yyyy = today.getFullYear();
    // const mm = String(today.getMonth() + 1).padStart(2, '0');
    // const dd = String(today.getDate()).padStart(2, '0');
    // const todayStr = `${yyyy}-${mm}-${dd}`;
    // $('#startDate').attr('min', todayStr);
    // $('#endDate').attr('min', todayStr);

    // Custom rule: end date should be after start date
    $.validator.addMethod("endDateAfterStart", function (value, element) {
        const start = $('#startDate').val();
        if (!start || !value) return true; // skip if one is missing
        return new Date(value) >= new Date(start);
    }, "End date must be after start date");

    //Custom rule: no spaces for coupon code
    $.validator.addMethod("noSpace", function (value, element) {
        return value === '' || value.indexOf(' ') < 0;
    }, "No spaces are allowed in the coupon code");

    //Custom rule: percentage can't be greater than 90
    $.validator.addMethod("percentageLimit", function (value, element) {
        const type = $("#discountType").val();
        if (type === "PERCENTAGE") {
            return parseFloat(value) <= 90;
        }
        return true;
    }, "Percentage discount cannot exceed 90%");

    // Initialize validation
    $("#couponForm").validate({
        rules: {
            code: {
                required: true,
                minlength: 3,
                maxlength: 50,
                noSpace: true
            },
            discount_type: {
                required: true
            },
            discount_value: {
                required: true,
                number: true,
                min: 1,
                percentageLimit: true,
            },
            min_purchase_amount: {
                required: true,
                number: true,
                min: 0
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
            usage_limit: {
                number: true,
                min: 1
            }
        },

        messages: {
            code: {
                required: "Please enter a coupon code",
                minlength: "At least 3 characters required",
                maxlength: "Maximum 50 characters allowed"
            },
            discount_type: {
                required: "Please select a discount type"
            },
            discount_value: {
                required: "Enter a discount value",
                number: "Enter a valid number",
                min: "Discount must be greater than 0"
            },
            min_purchase_amount: {
                required: "Minimum purchase is required",
                number: "Enter a valid number",
                min: "Minimum amount cannot be negative"
            },
            start_date: {
                required: "Start date is required",
                date: "Enter a valid date"
            },
            end_date: {
                required: "End date is required",
                date: "Enter a valid date",
                endDateAfterStart: "End date must be after start date"
            },
            usage_limit: {
                number: "Enter a valid number",
                min: "Usage limit must be at least 1"
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
            form.submit();
        }
    });
});

// Toggle status text
const statusToggle = document.getElementById('status');
const statusText = document.getElementById('statusText');

statusToggle.addEventListener('change', function () {
    statusText.textContent = this.checked ? 'Active' : 'Inactive';
});