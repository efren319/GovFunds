// Feedback Carousel Animation
function initCarousel() {
    const track = document.getElementById('feedbackTrack');
    
    if (track && track.children.length > 0) {
        let position = 0;
        const speed = 1; // pixels per frame
        const itemWidth = track.children[0].offsetWidth + 20; // item width + gap

        const interval = setInterval(() => {
            position -= speed;
            
            // Reset position for infinite loop
            if (Math.abs(position) >= itemWidth * (track.children.length / 2)) {
                position = 0;
            }
            
            track.style.transform = `translateX(${position}px)`;
        }, 30);
    }
}

// Budget Table Carousel Animation (Scrolling Upward)
function initBudgetTableCarousel() {
    const track = document.getElementById('budgetTableTrack');
    
    if (track && track.children.length > 0) {
        let position = 0;
        const speed = 0.5; // pixels per frame (slower than horizontal carousel)
        const itemHeight = track.children[0].offsetHeight; // height of each row
        
        setInterval(() => {
            position -= speed;
            
            // Reset position for infinite loop
            if (Math.abs(position) >= itemHeight * (track.children.length / 2)) {
                position = 0;
            }
            
            track.style.transform = `translateY(${position}px)`;
        }, 30);
    }
}

// Initialize carousel after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initCarousel, 100);
    setTimeout(initBudgetTableCarousel, 100);
});
