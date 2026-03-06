

// Add event listeners to size dropdowns
document.querySelectorAll('.size-dropdown').forEach(dropdown => {
    const addToCartBtn = dropdown.closest('.wishlist-card').querySelector('.btn-primary');
    
    // Disable add to cart by default if no size is selected
    if (!dropdown.value) {
        addToCartBtn.disabled = true;
    }
    
    dropdown.addEventListener('change', function() {
        if (this.value) {
            addToCartBtn.disabled = false;
            this.style.borderColor = ''; // Reset border color when a size is selected
        } else {
            addToCartBtn.disabled = true;
        }
    });
});


document.querySelectorAll('.wishlist-card').forEach(card => {
    const form = card.querySelector('form[action*="move-to-cart"]');
    const dropdown = card.querySelector('.size-dropdown');

    if (!form || !dropdown) return;

    form.addEventListener('submit', function (event) {
        if (!dropdown.value) {
            event.preventDefault();
            alert("Please select a size");
            return;
        }

        // ensure only ONE hidden field exists
        let hidden = form.querySelector('input[name="variant_id"]');
        if (!hidden) {
            hidden = document.createElement("input");
            hidden.type = "hidden";
            hidden.name = "variant_id";
            form.appendChild(hidden);
        }

        hidden.value = dropdown.value;
    });
});
