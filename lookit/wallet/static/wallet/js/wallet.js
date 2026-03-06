
// Add Money Modal
const addMoneyBtn = document.querySelector('.add-money-btn');
const addMoneyModal = document.getElementById('addMoneyModal');
const closeModalBtn = document.getElementById('closeModal');
const amountInput = document.getElementById('amountInput');
const amountOptions = document.querySelectorAll('.amount-option');
const proceedToPayBtn = document.getElementById('proceedToPayBtn');

// Open modal when Add Money button is clicked
if (addMoneyBtn) {
    addMoneyBtn.addEventListener('click', () => {
        addMoneyModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        setTimeout(() => amountInput.focus(), 100);
    });
}

// Close modal functions
function closeModal() {
    addMoneyModal.classList.remove('active');
    document.body.style.overflow = '';
}

if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);

// Close modal when clicking outside the modal content
addMoneyModal.addEventListener('click', (e) => {
    if (e.target === addMoneyModal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && addMoneyModal.classList.contains('active')) {
        closeModal();
    }
});

// Handle amount selection from quick options
amountOptions.forEach(option => {
    option.addEventListener('click', () => {
        const amount = option.textContent.replace('₹', '').trim();
        amountInput.value = amount;
        // validateAmount();
    });
});

// // Validate amount input
// function validateAmount() {
//     const amount = parseFloat(amountInput.value);
//     if (amount && amount > 0) {
//         addMoneySubmitBtn.disabled = false;
//     } else {
//         addMoneySubmitBtn.disabled = true;
//     }
// }

// Add input validation
if (amountInput) {
    // amountInput.addEventListener('input', validateAmount);

    // Prevent negative numbers
    amountInput.addEventListener('keydown', (e) => {
        if (e.key === '-' || e.key === 'e' || e.key === 'E') {
            e.preventDefault();
        }
    });
}

// Handle form submission
if (proceedToPayBtn) {
    proceedToPayBtn.addEventListener('click', () => {
        const amount = parseFloat(amountInput.value);
        if (amount && amount > 0) {
            createPaymentAjax(amount)
        }
    });
}


//CREATE RAZORPAY ORDER AND RETURN THE ORDER DETAILS USING AJAX
function createPaymentAjax(amount) {
    fetch(create_wallet_topup_razorpay_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({
            'amount': amount
        })
    }).then(response => response.json())
        .then(data => {
            console.log("ajax request success")

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
            closeModal()
            openRazorpayModal(options, data.failure_url)

        })
}

function openRazorpayModal(options, failure_url) {
    // initialise razorpay with the options.
    var rzp1 = new Razorpay(options);
    rzp1.open();

    // This captures hard failures like bank decline, invalid card, etc
    rzp1.on('payment.failed', function (response) {
        window.location.href = failure_url;
    });

}