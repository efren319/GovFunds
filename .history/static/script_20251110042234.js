document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('budgetChart').getContext('2d');

    // Get data from HTML data attributes
    const chartLabels = JSON.parse(document.getElementById('budgetChart').dataset.labels);
    const chartData = JSON.parse(document.getElementById('budgetChart').dataset.data);

    const budgetChart = new Chart(ctx, {
        type: 'pie',
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
                }
            }
        }
    });

    // Function to generate distinct colors
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
