document.addEventListener('DOMContentLoaded', () => {
    console.log('budget.js loaded');
    console.log('departmentsList:', typeof departmentsList !== 'undefined' ? departmentsList : 'NOT DEFINED');
    
    // Wait a moment for departmentsList to be available from template
    setTimeout(() => {
        if (typeof initDepartmentCarousel === 'function' && typeof departmentsList !== 'undefined' && departmentsList.length > 0) {
            // Transform data if needed - departmentsList contains objects with department and budget properties
            const depts = departmentsList.map(d => ({
                name: d.department,
                budget: d.budget
            }));
            console.log('Initializing carousel with:', depts);
            initDepartmentCarousel(depts);
        } else {
            console.log('Carousel not initialized - condition not met');
            console.log('  initDepartmentCarousel exists:', typeof initDepartmentCarousel === 'function');
            console.log('  departmentsList defined:', typeof departmentsList !== 'undefined');
            console.log('  departmentsList length:', typeof departmentsList !== 'undefined' ? departmentsList.length : 0);
        }
    }, 50);

    // Department Chart
    const deptCanvas = document.getElementById('departmentChart');
    if (deptCanvas) {
        const deptCtx = deptCanvas.getContext('2d');
        const deptLabels = JSON.parse(deptCanvas.dataset.labels);
        const deptData = JSON.parse(deptCanvas.dataset.data);

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
                        display: false
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

        // Populate Department Table
        const deptTotal = deptData.reduce((a, b) => a + b, 0);
        const deptTableBody = document.getElementById('deptTableBody');
        deptLabels.forEach((label, index) => {
            const amount = deptData[index];
            const percentage = ((amount / deptTotal) * 100).toFixed(1);
            const row = document.createElement('div');
            row.className = 'chart-table-row';
            row.innerHTML = `
                <div class="chart-table-col">${label}</div>
                <div class="chart-table-col">₱${amount.toLocaleString()}</div>
                <div class="chart-table-col">${percentage}%</div>
            `;
            deptTableBody.appendChild(row);
        });
    }

    // Region Chart
    const regCanvas = document.getElementById('regionChart');
    if (regCanvas) {
        const regCtx = regCanvas.getContext('2d');
        const regLabels = JSON.parse(regCanvas.dataset.labels);
        const regData = JSON.parse(regCanvas.dataset.data);

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
                        display: false
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

        // Populate Region Table
        const regTotal = regData.reduce((a, b) => a + b, 0);
        const regTableBody = document.getElementById('regionTableBody');
        regLabels.forEach((label, index) => {
            const amount = regData[index];
            const percentage = ((amount / regTotal) * 100).toFixed(1);
            const row = document.createElement('div');
            row.className = 'chart-table-row';
            row.innerHTML = `
                <div class="chart-table-col">${label}</div>
                <div class="chart-table-col">₱${amount.toLocaleString()}</div>
                <div class="chart-table-col">${percentage}%</div>
            `;
            regTableBody.appendChild(row);
        });
    }

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

    // Year selector functionality
    const yearSelect = document.getElementById('yearSelect');
    if (yearSelect) {
        yearSelect.addEventListener('change', function() {
            const year = this.value;
            window.location.href = `?year=${year}`;
        });
    }
});
