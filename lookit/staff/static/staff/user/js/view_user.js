// ============================================
// MAIN CONTENT FUNCTIONALITY
// ============================================

// Edit user info
function editUserInfo() {
    alert('Edit user information');
}

// Block user
function blockUser() {
    const modal = document.getElementById('blockModal');
    modal.classList.add('show');
}

function closeBlockModal() {
    const modal = document.getElementById('blockModal');
    modal.classList.remove('show');
}

function confirmBlockUser() {
    closeBlockModal();
}

// View all orders
function viewAllOrders() {
    alert('View all orders');
}

// Deduct amount from wallet
function deductAmount() {
    const amount = document.getElementById('walletAmount').value;
    if (!amount || amount <= 0) {
        alert('Please enter a valid amount');
        return;
    }
    if (confirm(`Are you sure you want to deduct $${amount} from user wallet?`)) {
        alert(`Amount $${amount} deducted from wallet`);
        document.getElementById('walletAmount').value = '';
    }
}

// Add amount to wallet
function addAmount() {
    const amount = document.getElementById('walletAmount').value;
    if (!amount || amount <= 0) {
        alert('Please enter a valid amount');
        return;
    }
    if (confirm(`Are you sure you want to add $${amount} to user wallet?`)) {
        alert(`Amount $${amount} added to wallet`);
        document.getElementById('walletAmount').value = '';
    }
}

// View all transactions
function viewAllTransactions() {
    alert('View all transactions');
}


// Close modal when clicking overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('show');
    }
});