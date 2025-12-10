document.addEventListener('DOMContentLoaded', () => {
    console.log('budget.js loaded');
    
    let deptChart = null;
    let regChart = null;
    
    function formatCurrency(amount) {
        return '₱' + amount.toLocaleString();
    }
    
    function generateColors(count) {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const hueVariation = -20 + (i / count) * 40;
            const hue = 168 + hueVariation;
            const lightness = 25 + (i % 5) * 15;
            const saturation = 25 + (i % 3) * 10;
            colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
        }
        return colors;
    }
    
    function updateCharts(year) {
        const data = BUDGET_DATA[year];
        if (!data) return;
        
        // Update annual budget display
        const annualDisplay = document.getElementById('annualBudgetDisplay');
        const yearDisplay = document.getElementById('selectedYearDisplay');
        if (annualDisplay) annualDisplay.textContent = formatCurrency(data.annual);
        if (yearDisplay) yearDisplay.textContent = year;
        
        // Extract sector data
        const sectorLabels = data.sectors.map(s => s.sector);
        const sectorData = data.sectors.map(s => s.budget);
        
        // Extract region data
        const regionLabels = data.regions.map(r => r.region);
        const regionData = data.regions.map(r => r.budget);
        
        // Update Department Chart
        const deptCanvas = document.getElementById('departmentChart');
        if (deptCanvas) {
            const deptCtx = deptCanvas.getContext('2d');
            
            if (deptChart) {
                deptChart.destroy();
            }
            
            const centerTextPlugin = {
                id: 'centerText',
                afterDraw(chart) {
                    const {ctx, chartArea: {width, height}} = chart;
                    ctx.save();
                    ctx.font = `${Math.min(width, height) / 20}px sans-serif`;
                    ctx.fillStyle = 'black';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText('Budget by Sector', width / 2, height / 2);
                    ctx.restore();
                }
            };

            deptChart = new Chart(deptCtx, {
                type: 'doughnut',
                data: {
                    labels: sectorLabels,
                    datasets: [{
                        data: sectorData,
                        backgroundColor: generateColors(sectorData.length),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '50%',
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return formatCurrency(context.raw);
                                }
                            }
                        }
                    }
                },
                plugins: [centerTextPlugin]
            });

            // Populate Department Table
            const deptTotal = sectorData.reduce((a, b) => a + b, 0);
            const deptTableBody = document.getElementById('deptTableBody');
            if (deptTableBody) {
                deptTableBody.innerHTML = '';
                sectorLabels.forEach((label, index) => {
                    const amount = sectorData[index];
                    const percentage = ((amount / deptTotal) * 100).toFixed(1);
                    const row = document.createElement('div');
                    row.className = 'chart-table-row';
                    row.innerHTML = `
                        <div class="chart-table-col">${label}</div>
                        <div class="chart-table-col">${formatCurrency(amount)}</div>
                        <div class="chart-table-col">${percentage}%</div>
                    `;
                    deptTableBody.appendChild(row);
                });
            }
        }

        // Update Region Chart
        const regCanvas = document.getElementById('regionChart');
        if (regCanvas) {
            const regCtx = regCanvas.getContext('2d');
            
            if (regChart) {
                regChart.destroy();
            }

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

            regChart = new Chart(regCtx, {
                type: 'doughnut',
                data: {
                    labels: regionLabels,
                    datasets: [{
                        data: regionData,
                        backgroundColor: generateColors(regionData.length),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '50%',
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return formatCurrency(context.raw);
                                }
                            }
                        }
                    }
                },
                plugins: [centerTextPlugin2]
            });

            // Populate Region Table
            const regTotal = regionData.reduce((a, b) => a + b, 0);
            const regTableBody = document.getElementById('regionTableBody');
            if (regTableBody) {
                regTableBody.innerHTML = '';
                regionLabels.forEach((label, index) => {
                    const amount = regionData[index];
                    const percentage = ((amount / regTotal) * 100).toFixed(1);
                    const row = document.createElement('div');
                    row.className = 'chart-table-row';
                    row.innerHTML = `
                        <div class="chart-table-col">${label}</div>
                        <div class="chart-table-col">${formatCurrency(amount)}</div>
                        <div class="chart-table-col">${percentage}%</div>
                    `;
                    regTableBody.appendChild(row);
                });
            }
        }
        
        // Update rotating department display
        if (typeof initDepartmentCarousel === 'function' && data.sectors.length > 0) {
            const depts = data.sectors.map(d => ({
                name: d.sector,
                budget: d.budget
            }));
            initDepartmentCarousel(depts);
        }
    }
    
    // Initialize with default year (2025)
    const yearSelect = document.getElementById('yearSelect');
    const initialYear = yearSelect ? parseInt(yearSelect.value) : 2025;
    
    // Wait for BUDGET_DATA to be available
    setTimeout(() => {
        updateCharts(initialYear);
    }, 50);

    // Year selector functionality - update charts without page reload
    if (yearSelect) {
        yearSelect.addEventListener('change', function() {
            const year = parseInt(this.value);
            updateCharts(year);
        });
    }
});
