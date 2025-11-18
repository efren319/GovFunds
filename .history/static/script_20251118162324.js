// Feedback Carousel Animation
function initCarousel() {
    const track = document.getElementById('feedbackTrack');
    if (track && track.children.length > 0) {
        let position = 0;
        const speed = 1; // pixels per frame
        const itemWidth = track.children[0].offsetWidth + 20; // item width + gap

        setInterval(() => {
            position -= speed;
            
            // Reset position for infinite loop
            if (Math.abs(position) >= itemWidth * (track.children.length / 2)) {
                position = 0;
            }
            
            track.style.transform = `translateX(${position}px)`;
        }, 30);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initCarousel();
    
    const ctx = document.getElementById('budgetChart').getContext('2d');

    const chartLabels = JSON.parse(document.getElementById('budgetChart').dataset.labels);
    const chartData = JSON.parse(document.getElementById('budgetChart').dataset.data);

    const centerTextPlugin = {
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
            cutout: '50%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 20,
                        boxHeight: 20
                    }
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
        },
        plugins: [centerTextPlugin]
    });

    function generateColors(count) {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const hue = Math.floor((i / count) * 360);
            colors.push(`hsl(${hue}, 70%, 60%)`); // ensures unique, visible colors
        }
        return colors;
    }
});
