// ---ADDRESS SELECTION ----------------------------------------
let selectedAddressId = null

//on page load put default address as selected address
document.addEventListener("DOMContentLoaded", function () {
    const hiddenInput = document.getElementById("defaultAddressHidden")
    if(hiddenInput){
        selectedAddressId = hiddenInput.value
    }else{
        selectedAddressId = 0
    }
    console.log(selectedAddressId)
    document.getElementById('selectedAddressId').value = selectedAddressId
});


function selectAddress(e, div, addressId){
    console.log("call aaayi")
    // Don't trigger for buttons inside the address option
    if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
        return;
    }
    selectedAddressId = addressId
    
    document.querySelectorAll('.address-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    document.getElementById('selectedAddressId').value = selectedAddressId
    div.classList.add('selected');
    const radio = div.querySelector('input[type="radio"]');
    if (radio) {
        radio.checked = true;
    }
}






