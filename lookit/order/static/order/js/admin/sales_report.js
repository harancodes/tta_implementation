let isProgrammaticDateChange = false;


// Date range button functionality
const dateRangeBtns = document.querySelectorAll('.date-range-btn');
const rangeTypeHiddenInput = document.getElementById('rangeInput')

function activateCustomRange() {
    dateRangeBtns.forEach(b => b.classList.remove('active'));

    const customBtn = document.querySelector('.date-range-btn[value="custom"]');
    if (customBtn) {
        customBtn.classList.add('active');
    }

    rangeTypeHiddenInput.value = 'custom';
}

flatpickr(".date-picker", {
    dateFormat: "Y-m-d",
    allowInput: true,
    onChange: function () {
        if (isProgrammaticDateChange) return;

        activateCustomRange();
    }
});



dateRangeBtns.forEach(btn => {
    btn.addEventListener('click', function () {
        dateRangeBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        rangeTypeHiddenInput.value = this.value;

        const range = this.textContent.trim();
        const today = new Date();
        const fromDate = document.getElementById('fromDate');
        const toDate = document.getElementById('toDate');

        isProgrammaticDateChange = true;

        if (range === 'Today') {
            fromDate._flatpickr.setDate(today, true);
            toDate._flatpickr.setDate(today, true);
        } else if (range === 'This Week') {
            const firstDay = new Date(today);
            firstDay.setDate(today.getDate() - today.getDay());
            fromDate._flatpickr.setDate(firstDay, true);
            toDate._flatpickr.setDate(new Date(), true);
        } else if (range === 'This Month') {
            const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
            fromDate._flatpickr.setDate(firstDay, true);
            toDate._flatpickr.setDate(new Date(), true);
        } else if (range === 'This Year') {
            const firstDay = new Date(today.getFullYear(), 0, 1);
            fromDate._flatpickr.setDate(firstDay, true);
            toDate._flatpickr.setDate(new Date(), true);
        }

        isProgrammaticDateChange = false;
    });
});


// Set default date range to today
document.addEventListener('DOMContentLoaded', function () {
    const today = new Date();
    const fromDate = document.getElementById('fromDate');
    const toDate = document.getElementById('toDate');

    if (fromDate?._flatpickr && !fromDate.value) {
        fromDate._flatpickr.setDate(today, true);
    }

    if (toDate?._flatpickr && !toDate.value) {
        toDate._flatpickr.setDate(today, true);
    }
});

