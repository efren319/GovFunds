let currentProjectId = null;
const allRegions = JSON.parse(document.currentScript?.dataset.regions || '[]');

// Add event listeners to edit buttons
document.querySelectorAll('.edit-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const projectId = this.dataset.projectId;
    openEditModal(parseInt(projectId));
  });
});

async function openEditModal(projectId) {
  currentProjectId = projectId;
  try {
    const response = await fetch(`/api/project/${projectId}`);
    const project = await response.json();
    
    // Populate form with project data
    document.querySelector('input[name="name"]').value = project.name;
    document.querySelector('select[name="project_sector"]').value = project.project_sector;
    document.querySelector('select[name="region"]').value = project.region;
    document.querySelector('select[name="status"]').value = project.status;
    document.querySelector('input[name="allocated_budget"]').value = project.allocated_budget;
    document.querySelector('input[name="spent"]').value = project.spent;
    document.querySelector('textarea[name="description"]').value = project.description || '';
    
    // Populate regions
    populateRegions();
    
    // Show modal
    document.getElementById('editModal').style.display = 'flex';
  } catch (error) {
    console.error('Error loading project:', error);
    alert('Error loading project data');
  }
}

function closeEditModal(event) {
  if (event && event.target !== document.getElementById('editModal')) return;
  document.getElementById('editModal').style.display = 'none';
  currentProjectId = null;
}

function populateRegions() {
  const select = document.getElementById('regionSelect');
  const currentValue = select.value;
  
  // Clear existing options (except the first one)
  while (select.options.length > 1) {
    select.remove(1);
  }
  
  // Add all regions
  allRegions.forEach(region => {
    const option = document.createElement('option');
    option.value = region;
    option.textContent = region;
    select.appendChild(option);
  });
  
  select.value = currentValue;
}

document.getElementById('editProjectForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(document.getElementById('editProjectForm'));
  
  try {
    const response = await fetch(`/project/${currentProjectId}/edit`, {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      location.reload();
    } else {
      alert('Error updating project');
    }
  } catch (error) {
    console.error('Error updating project:', error);
    alert('Error updating project');
  }
});

// Close modal when clicking outside
document.getElementById('editModal')?.addEventListener('click', function(e) {
  if (e.target === this) {
    closeEditModal();
  }
});
