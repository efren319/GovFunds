document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('budgetChart').getContext('2d');

    const chartLabels = JSON.parse(document.getElementById('budgetChart').dataset.labels);
    const chartData = JSON.parse(document.getElementById('budgetChart').dataset.data);

    // Create donut chart
    const budgetChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Allocated Budget',
                data: chartData,
                backgroundColor: generateColors(chartData.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            cutout: '50%', // Creates white circle in the middle
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let value = context.raw;
                            return '₱' + value.toLocaleString();
                        }
                    }
                },
                // Center text plugin
                beforeDraw: function(chart) {
                    const width = chart.width,
                          height = chart.height,
                          ctx = chart.ctx;
                    ctx.restore();
                    const fontSize = (height / 114).toFixed(2);
                    ctx.font = fontSize + "em sans-serif";
                    ctx.textBaseline = "middle";

                    const text = "Budget by Region",
                          textX = Math.round((width - ctx.measureText(text).width) / 2),
                          textY = height / 2;

                    ctx.fillText(text, textX, textY);
                    ctx.save();
                }
            }
        },
        plugins: [{
            id: 'centerText',
            beforeDraw: function(chart) {
                const width = chart.width,
                      height = chart.height,
                      ctx = chart.ctx;
                ctx.restore();
                const fontSize = (height / 114).toFixed(2);
                ctx.font = fontSize + "em sans-serif";
                ctx.textBaseline = "middle";
                const text = "Budget by Region",
                      textX = Math.round((width - ctx.measureText(text).width) / 2),
                      textY = height / 2;
                ctx.fillText(text, textX, textY);
                ctx.save();
            }
        }]
    });

    // Function to generate colors dynamically
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
