// Static budget data - hardcoded since it doesn't change
const BUDGET_DATA = {
  2025: {
    annual: 6095900000000,
    sectors: [
      { sector: 'Road Infrastructure', budget: 541980000000 },
      { sector: 'Special Infrastructure Projects', budget: 330000000000 },
      { sector: 'Flood Control and Drainage', budget: 257060000000 },
      { sector: 'Public Buildings', budget: 113522058000 },
      { sector: 'Water Resources and Irrigation', budget: 42570000000 },
      { sector: 'Bridge Infrastructure', budget: 38000000000 },
      { sector: 'Local Infrastructure Support', budget: 25000000000 },
      { sector: 'Disaster Response and Rehabilitation', budget: 10000000000 }
    ],
    regions: [
      { region: 'National Capital Region', budget: 834600000000 },
      { region: 'Region III', budget: 420600000000 },
      { region: 'Region IV-A', budget: 395600000000 },
      { region: 'Region V', budget: 257300000000 },
      { region: 'Region VII', budget: 255900000000 },
      { region: 'Region VI', budget: 236100000000 },
      { region: 'Region VIII', budget: 209400000000 },
      { region: 'Region I', budget: 198700000000 },
      { region: 'Region X', budget: 195700000000 },
      { region: 'Region IV-B', budget: 184600000000 },
      { region: 'Region II', budget: 175000000000 },
      { region: 'BARMM', budget: 172400000000 },
      { region: 'Region XI', budget: 172500000000 },
      { region: 'Region IX', budget: 149300000000 },
      { region: 'Caraga', budget: 138900000000 },
      { region: 'Region XII', budget: 137800000000 },
      { region: 'Cordillera Administrative Region', budget: 106000000000 }
    ]
  },
  2024: {
    annual: 5705700000000,
    sectors: [
      { sector: 'Special Infrastructure Projects', budget: 410991162000 },
      { sector: 'Flood Control and Drainage', budget: 244577911000 },
      { sector: 'Road Infrastructure', budget: 132328352000 },
      { sector: 'Public Buildings', budget: 100214102000 },
      { sector: 'Water Resources and Irrigation', budget: 74903429000 },
      { sector: 'Local Infrastructure Support', budget: 39343250000 },
      { sector: 'Bridge Infrastructure', budget: 24755275000 },
      { sector: 'Disaster Response and Rehabilitation', budget: 1000000000 }
    ],
    regions: [
      { region: 'Cordillera Administrative Region', budget: 867228911000 },
      { region: 'National Capital Region', budget: 532008065000 },
      { region: 'Region IV-A', budget: 369230365000 },
      { region: 'Region IV-B', budget: 341101910000 },
      { region: 'Region V', budget: 234040470000 },
      { region: 'Region VII', budget: 228181764000 },
      { region: 'Region VI', budget: 222399947000 },
      { region: 'Region VIII', budget: 205946394000 },
      { region: 'Region X', budget: 190071333000 },
      { region: 'Region I', budget: 180565920000 },
      { region: 'Region XI', budget: 162666370000 },
      { region: 'Region III', budget: 160174535000 },
      { region: 'BARMM', budget: 149440406000 },
      { region: 'Region IX', budget: 140072215000 },
      { region: 'Region XII', budget: 127046390000 },
      { region: 'Caraga', budget: 124270792000 },
      { region: 'Region II', budget: 97668044000 }
    ]
  },
  2023: {
    annual: 5278700000000,
    sectors: [
      { sector: 'Special Infrastructure Projects', budget: 388286983000 },
      { sector: 'Flood Control and Drainage', budget: 182989695000 },
      { sector: 'Road Infrastructure', budget: 116252873000 },
      { sector: 'Public Buildings', budget: 79409974000 },
      { sector: 'Local Infrastructure Support', budget: 37285405000 },
      { sector: 'Bridge Infrastructure', budget: 29333447000 },
      { sector: 'Water Resources and Irrigation', budget: 15413692000 },
      { sector: 'Disaster Response and Rehabilitation', budget: 11000000000 }
    ],
    regions: [
      { region: 'National Capital Region', budget: 887000000000 },
      { region: 'Region III', budget: 321100000000 },
      { region: 'Region IV-A', budget: 318700000000 },
      { region: 'Region V', budget: 212800000000 },
      { region: 'Region VII', budget: 212000000000 },
      { region: 'Region VI', budget: 203500000000 },
      { region: 'Region VIII', budget: 177400000000 },
      { region: 'Region X', budget: 175000000000 },
      { region: 'Region I', budget: 169900000000 },
      { region: 'Region XI', budget: 149100000000 },
      { region: 'Region II', budget: 144700000000 },
      { region: 'Region IV-B', budget: 134200000000 },
      { region: 'BARMM', budget: 130300000000 },
      { region: 'Region IX', budget: 126800000000 },
      { region: 'Region XII', budget: 116400000000 },
      { region: 'Caraga', budget: 109300000000 },
      { region: 'Cordillera Administrative Region', budget: 98500000000 }
    ]
  }
};

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
