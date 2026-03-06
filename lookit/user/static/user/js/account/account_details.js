 
// Copy referral code functionality
const copyBtn = document.querySelector('.action-icon-btn[title="Copy"]');
if (copyBtn) {
    copyBtn.addEventListener('click', function() {
        const referralCode = document.querySelector('.referral-code').textContent;
        navigator.clipboard.writeText(referralCode).then(function() {
            // Visual feedback
            const originalSvg = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>';
            setTimeout(function() {
                copyBtn.innerHTML = originalSvg;
            }, 2000);
        });
    });
}
 