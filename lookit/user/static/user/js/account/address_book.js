
// DOM Elements
const modalTitle = document.getElementById('modalTitle');
const addressIdInput = document.getElementById('addressId');
const addressGrid = document.getElementById('addressGrid');
const addressLabels = document.querySelectorAll('input[name="addressLabel"]');
const customLabelContainer = document.querySelector('.custom-label');


// ==============================
// Delete Modal Functions
// ==============================
let currentStyleId = null;

function openDeleteModal(address_id) {
    console.log("call is here")
    console.log(address_id)
    const modal = document.getElementById('deleteModal'+address_id);
    if (modal) modal.classList.add('show');
}

function closeDeleteModal(address_id) {
    const modal = document.getElementById('deleteModal'+address_id);
    if (modal) modal.classList.remove('show');
}


