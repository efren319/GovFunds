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
