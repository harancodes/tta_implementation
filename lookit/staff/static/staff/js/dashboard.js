// Animate chart bars on load
window.addEventListener('load', () => {
    const bars = document.querySelectorAll('.category-bar');
    bars.forEach((bar, index) => {
        setTimeout(() => {
            bar.style.width = bar.style.width || '0%';
        }, index * 100);
    });
});

// Toggle KPI cards on mobile
function toggleKPICards() {
    const hiddenCards = document.querySelectorAll('.kpi-card.hidden-mobile');
    const toggleBtn = document.getElementById('kpiToggle');
    const toggleText = document.getElementById('toggleText');
    
    hiddenCards.forEach(card => {
        card.classList.toggle('show');
    });
    
    // Update button text and active state
    if (hiddenCards[0].classList.contains('show')) {
        toggleText.textContent = 'Show Less';
        toggleBtn.classList.add('active');
    } else {
        toggleText.textContent = 'Show More';
        toggleBtn.classList.remove('active');
    }
}


//CHART JS SCRIPT
document.addEventListener("DOMContentLoaded", function () {
  console.log(labels)
  const ctx = document.getElementById('salesChart');
  if (!ctx) {
    console.error("Canvas element #salesChart not found!");
    return;
  }

  const data = {
    labels: labels,
    datasets: [{
      label: 'Revenue (₹)',
      data: dataValues,
      borderColor: '#6366f1',
      backgroundColor: 'rgba(99, 102, 241, 0.6)',
      borderWidth: 2,
      borderRadius: 8,
      borderSkipped: false,
      barThickness: 40,
    }]
  };

  const config = {
    type: 'bar',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: upper_limit, // 👈 set upper limit
          grid: { color: '#f3f4f6' },
          ticks: { color: '#6b7280', stepSize: step },
        },
        x: {
          ticks: { color: '#6b7280' },
          grid: { display: false },
        }
      },
      plugins: {
        legend: { display: false },
        title: {
          display: false
        },
        tooltip: {
          backgroundColor: '#1f2937',
          titleColor: '#fff',
          bodyColor: '#d1d5db',
          borderColor: '#4f46e5',
          borderWidth: 1,
        }
      },
      animation: {
        duration: 1200,
        easing: 'easeOutQuart',
      }
    }
  };

  new Chart(ctx, config);
});