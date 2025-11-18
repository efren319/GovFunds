// Department Carousel Rotation
function initDepartmentCarousel(departmentsData) {
    let currentDeptIndex = 0;
    const deptNameEl = document.getElementById('deptName');
    const deptBudgetEl = document.getElementById('deptBudget');

    if (!deptNameEl || !deptBudgetEl || departmentsData.length === 0) {
        return;
    }

    // Set initial fade in
    deptNameEl.style.opacity = '1';
    deptBudgetEl.style.opacity = '1';
    deptNameEl.style.transition = 'opacity 0.5s ease-in-out';
    deptBudgetEl.style.transition = 'opacity 0.5s ease-in-out';

    function updateDepartmentDisplay() {
        // Fade out
        deptNameEl.style.opacity = '0';
        deptBudgetEl.style.opacity = '0';

        // Update after fade out
        setTimeout(() => {
            const dept = departmentsData[currentDeptIndex];
            deptNameEl.textContent = dept.name;
            deptBudgetEl.textContent = '₱' + dept.budget.toLocaleString();
            
            // Fade in
            deptNameEl.style.opacity = '1';
            deptBudgetEl.style.opacity = '1';
            
            currentDeptIndex = (currentDeptIndex + 1) % departmentsData.length;
        }, 250);
    }

    // Initial display
    updateDepartmentDisplay();

    // Rotate every 3 seconds
    setInterval(updateDepartmentDisplay, 3000);
}

// Initialize Budget Charts and Functionality
function initBudgetPage() {
    // Department Carousel Data
    const departmentsList = [
        ...JSON.parse(document.getElementById('departmentsList').textContent)
    ];

    // Initialize carousel
    initDepartmentCarousel(departmentsList);

    // Department Chart
    const deptCtx = document.getElementById('departmentChart').getContext('2d');
    const deptLabels = JSON.parse(document.getElementById('departmentChart').dataset.labels);
    const deptData = JSON.parse(document.getElementById('departmentChart').dataset.data);

    const centerTextPlugin = {
        id: 'centerText',
        afterDraw(chart) {
            const {ctx, chartArea: {width, height}} = chart;
            ctx.save();
            ctx.font = `${Math.min(width, height) / 20}px sans-serif`;
            ctx.fillStyle = 'black';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('Budget by Department', width / 2, height / 2);
            ctx.restore();
        }
    };

    const deptChart = new Chart(deptCtx, {
        type: 'doughnut',
        data: {
            labels: deptLabels,
            datasets: [{
                data: deptData,
                backgroundColor: generateColors(deptData.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '50%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: { boxWidth: 15, boxHeight: 15 }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '₱' + context.raw.toLocaleString();
                        }
                    }
                }
            }
        },
        plugins: [centerTextPlugin]
    });

    // Region Chart
    const regCtx = document.getElementById('regionChart').getContext('2d');
    const regLabels = JSON.parse(document.getElementById('regionChart').dataset.labels);
    const regData = JSON.parse(document.getElementById('regionChart').dataset.data);

    const centerTextPlugin2 = {
        id: 'centerText',
        afterDraw(chart) {
            const {ctx, chartArea: {width, height}} = chart;
            ctx.save();
            ctx.font = `${Math.min(width, height) / 20}px sans-serif`;
            ctx.fillStyle = 'black';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('Budget by Region', width / 2, height / 2);
            ctx.restore();
        }
    };

    const regChart = new Chart(regCtx, {
        type: 'doughnut',
        data: {
            labels: regLabels,
            datasets: [{
                data: regData,
                backgroundColor: generateColors(regData.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '50%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: { boxWidth: 15, boxHeight: 15 }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '₱' + context.raw.toLocaleString();
                        }
                    }
                }
            }
        },
        plugins: [centerTextPlugin2]
    });

    // Year selector functionality
    const yearSelect = document.getElementById('yearSelect');
    if (yearSelect) {
        yearSelect.addEventListener('change', function() {
            const year = this.value;
            window.location.href = `?year=${year}`;
        });
    }
}

// Generate HSL colors for charts
function generateColors(count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        const hueVariation = -20 + (i / count) * 40;
        const hue = 168 + hueVariation;
        const lightness = 25 + (i % 5) * 15;
        const saturation = 70 + (i % 3) * 10;
        colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
    }
    return colors;
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initBudgetPage);

