document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('budgetChart').getContext('2d');

    const chartLabels = JSON.parse(document.getElementById('budgetChart').dataset.labels);
    const chartData = JSON.parse(document.getElementById('budgetChart').dataset.data);

    // Center text plugin
    const centerTextPlugin = {
        id: 'centerText',
        afterDraw(chart) {
            const {ctx, chartArea: {width, height}} = chart;
            ctx.save();
            ctx.font = '16px sans-serif';
            ctx.fillStyle = 'black';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('Budget by Region', width / 2, height / 2);
            ctx.restore();
        }
    };

    const budgetChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartLabels,
            datasets: [{
                data: chartData,
                backgroundColor: generateColors(chartData.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '50%', // creates white circle in middle
            plugins: {
                legend: { position: 'right' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let value = context.raw;
                            return '₱' + value.toLocaleString();
                        }
                    }
                }
            }
        },
        plugins: [centerTextPlugin]
    });

    function generateColors(count) {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const r = Math.floor(Math.random() * 255);
            const g = Math.floor(Math.random() * 255);
            const b = Math.floor(Math.random() * 255);
            colors.push(`rgba(${r}, ${g}, ${b}, 0.6)`);
        }
        return colors;
    }
});
