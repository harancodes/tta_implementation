
// Quantity controls
// document.querySelectorAll('.quantity-btn').forEach(button => {
//     button.addEventListener('click', function() {
//         const quantityElement = this.parentElement.querySelector('.quantity');
//         let quantity = parseInt(quantityElement.textContent);
        
//         if (this.textContent === '+' && quantity < 4) {
//             quantityElement.textContent = quantity + 1;
//         } else if (this.textContent === '-' && quantity > 1) {
//             quantityElement.textContent = quantity - 1;
//         }
//     });
// });

function updateQuantity(btn, cartId, variantId, csrfToken){
        const quantityElement = btn.parentElement.querySelector('.quantity');
        let quantity = parseInt(quantityElement.textContent);
        let new_quantity = null
        
        if (btn.textContent === '+' && quantity < MAX_CART_QUANTITY) {
            new_quantity = quantity + 1
        } else if (btn.textContent === '-' && quantity > 1) {
            new_quantity = quantity - 1
        }
        if(new_quantity){
            submitQuantity(cartId, variantId, new_quantity, csrfToken, quantityElement)
        }
        
}

function submitQuantity(cartId, variantId, quantity, csrfToken, quantityElement) {
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            cart_id: cartId,
            variant_id: variantId,
            new_quantity: Number(quantity),
        }),
    })
        .then(response => response.json())
        .then(data => {
            
            if (data.error) {
                console.log("something wrong")
                quantityElement.textContent = data.quantity;
                showToast("#toastError");

            }else{
                cartSummary = data.cart_summary
                quantityElement.textContent = data.new_quantity;
                document.getElementById('sub_total').innerText = "₹"+cartSummary.sub_total
                document.getElementById('total_amount').innerText = "₹"+cartSummary.grand_total
                const totalDiscount = document.getElementById('cartTotalDiscount')
                if(totalDiscount){
                    totalDiscount.innerText = "-₹"+cartSummary.offer_discount
                }
                const couponDiscount = document.getElementById('appliedCouponDiscount')
                if(couponDiscount){
                    couponDiscount.innerText = cartSummary.coupon_discount
                }
                //update subtotal of each product
                Object.values(data.cart_items).forEach(item => {
                    // console.log(item)
                    document.getElementById("cartItemQuantity"+item.id).innerText = item.quantity+"× "
                    document.getElementById('subTotalProduct'+item.id).innerText = "₹"+item.sub_total
                });     
            }
            
            
        });
}

// Remove item
document.querySelectorAll('.remove-btn').forEach(button => {
    button.addEventListener('click', function() {
        //this.closest('.cart-item').remove();
    });
});


// Toggle Coupon Section
const toggleCouponBtn = document.getElementById('toggleCouponBtn');
const couponSection = document.getElementById('couponSection');

if (toggleCouponBtn) {
    toggleCouponBtn.addEventListener('click', () => {
        couponSection.style.display = couponSection.style.display === 'none' ? 'block' : 'none';
        toggleCouponBtn.classList.toggle('active');
    });
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


//Coupon related
// Example JS for showing/removing applied coupon UI
// document.addEventListener('DOMContentLoaded', () => {
//     const appliedBox = document.getElementById('appliedCouponBox');
//     const appliedCode = document.getElementById('appliedCouponCodeText');
//     const appliedDiscount = document.getElementById('appliedCouponDiscountText');
//     const removeBtn = document.getElementById('removeCouponBtn');

//     // Simulate coupon applied
//     function showAppliedCoupon(code, discount) {
//         appliedCode.textContent = code;
//         appliedDiscount.textContent = discount;
//         appliedBox.style.display = 'flex';
//     }

//     // Remove coupon
//     removeBtn.addEventListener('click', () => {
//         appliedBox.style.display = 'none';
//         document.getElementById('couponCode').value = '';
//         document.getElementById('couponMessage').textContent = 'Coupon removed.';
//         document.getElementById('couponMessage').className = 'coupon-message success';
//         // TODO: Add your backend remove logic (AJAX or form submission)
//     });

//     // Example usage:
//     // showAppliedCoupon("WELCOME10", "150");
// });
