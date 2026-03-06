
// Show selected tab content
function showTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected tab content
    document.getElementById(tabId).classList.add('active');

    // Add active class to clicked tab
    event.currentTarget.classList.add('active');
}

// Format card number with spaces
function formatCardNumber(input) {
    // Remove all non-digit characters
    let value = input.value.replace(/\D/g, '');

    // Add space after every 4 digits
    value = value.replace(/(\d{4})(?=\d)/g, '$1 ');

    // Update input value
    input.value = value.trim();
}

// Format expiry date with slash
function formatExpiryDate(input) {
    let value = input.value.replace(/\D/g, '');

    if (value.length > 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }

    input.value = value;
}

//CREATE RAZORPAY ORDER AND RETURN THE ORDER DETAILS USING AJAX
function createPaymentAjax() {
    fetch(create_razorpay_order_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({
            'order_id': order_id
        })
    }).then(response => response.json())
        .then(data => {
            console.log("ajax request success")
            if (data.failed) {
                console.log("Failed")
                location.reload();
            } else {
                var options = {
                    // Enter the Key ID generated from the Dashboard
                    key: data.razorpay_merchant_key,

                    // Amount is in currency subunits.
                    // Default currency is INR. Hence, 
                    // 50000 refers to 50000 paise
                    amount: data.razorpay_amount,
                    currency: data.currency,

                    // Your/store name.
                    name: data.name,

                    // Pass the `id` obtained in the response of Step 1
                    order_id: data.razorpay_order_id,
                    callback_url: data.callback_url,

                };
                openRazorpayModal(options)
            }
        })
}

function openRazorpayModal(options) {
    console.log(payment_failed_url)
    // initialise razorpay with the options.
    var rzp1 = new Razorpay(options);
    rzp1.open();

    //This captures hard failures like bank decline, invalid card, etc
    rzp1.on('payment.failed', function (response) {
        window.location.href = payment_failed_url;
    });

}

function openWalletConfirm() {
    document.getElementById('walletConfirmModal').classList.add('active');
    document.body.style.overflow = "hidden";
}

function closeWalletConfirm() {
    document.getElementById('walletConfirmModal').classList.remove('active');
    document.body.style.overflow = "";
}






