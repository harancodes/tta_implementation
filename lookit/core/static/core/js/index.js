function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value
        || document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
}


function toggleWishlist(event, button) {
    event.preventDefault();   // stop <a> navigation
    event.stopPropagation();  // stop bubbling to parent

    const productId = button.dataset.productId;
    //wishlist count badge in navbar
    const wishlistCount = document.getElementById('wishlistCount')
    let count = Number(wishlistCount.innerText)
    console.log(count)

    fetch(toggle_wishlist_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Request failed');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'added') {
            button.classList.add('active');
            wishlistCount.innerText = count + 1
        } else if (data.status === 'removed') {
            button.classList.remove('active');
            wishlistCount.innerText = count - 1
        } else if(data.status == 'failed'){
            console.log("something went wrong")
        }
    })
    .catch(error => {
        console.error(error);
        // optional: show toast
    });
}