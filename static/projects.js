// projects.js - Projects page functionality

let currentProjectId = null;
let allRegions = [];

// Initialize the projects page
function initProjectsPage(regions) {
  allRegions = regions;
  
  // Add event listeners to edit buttons
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const projectId = this.dataset.projectId;
      openEditModal(parseInt(projectId));
    });
  });

  // Form submit handler
  const editForm = document.getElementById('editProjectForm');
  if (editForm) {
    editForm.addEventListener('submit', handleEditFormSubmit);
  }

  // Close modal when clicking outside
  const editModal = document.getElementById('editModal');
  if (editModal) {
    editModal.addEventListener('click', function(e) {
      if (e.target === this) {
        closeEditModal();
      }
    });
  }

  // File upload preview for edit modal
  const editFileInput = document.getElementById('editProjectImageInput');
  if (editFileInput) {
    editFileInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      const preview = document.getElementById('currentImagePreview');
      const previewImage = document.getElementById('editImagePreview');
      const fileName = document.getElementById('editFileName');
      const uploadLabel = document.getElementById('editUploadLabel');
      
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          previewImage.src = e.target.result;
          fileName.textContent = file.name;
          preview.style.display = 'flex';
          uploadLabel.style.display = 'none';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Initialize scroll animation for project cards
  initScrollAnimation();
}

// Scroll animation for project cards
function initScrollAnimation() {
  const cards = document.querySelectorAll('.project-card');
  
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // Add visible class when in view
        entry.target.classList.add('visible');
      } else {
        // Remove visible class when out of view to reset animation
        entry.target.classList.remove('visible');
      }
    });
  }, observerOptions);

  cards.forEach(card => {
    observer.observe(card);
  });
}

// Filter and Sort Projects
function filterAndSortProjects() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  const sortBy = document.getElementById('sortBy').value;
  const sortOrder = document.getElementById('sortOrder').value;
  const statusFilter = document.getElementById('statusFilter').value.toLowerCase();
  const regionFilter = document.getElementById('regionFilter').value.toLowerCase();
  const sectorFilter = document.getElementById('sectorFilter').value.toLowerCase();
  
  const grid = document.getElementById('projectsGrid');
  const cards = Array.from(grid.querySelectorAll('.project-card'));
  
  // Filter cards
  let visibleCount = 0;
  cards.forEach(card => {
    const name = card.dataset.name || '';
    const sector = card.dataset.sector || '';
    const region = card.dataset.region || '';
    const status = card.dataset.status || '';
    
    const matchesSearch = name.includes(searchTerm) || 
                         sector.includes(searchTerm) || 
                         region.includes(searchTerm);
    const matchesStatus = !statusFilter || status === statusFilter;
    const matchesRegion = !regionFilter || region === regionFilter;
    const matchesSector = !sectorFilter || sector === sectorFilter;
    
    if (matchesSearch && matchesStatus && matchesRegion && matchesSector) {
      card.style.display = '';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });
  
  // Show/hide no results message
  document.getElementById('noResults').style.display = visibleCount === 0 ? 'block' : 'none';
  
  // Sort visible cards
  const visibleCards = cards.filter(card => card.style.display !== 'none');
  
  visibleCards.sort((a, b) => {
    let aVal, bVal;
    
    switch(sortBy) {
      case 'name':
        aVal = a.dataset.name || '';
        bVal = b.dataset.name || '';
        break;
      case 'date':
        aVal = a.dataset.date || '9999-99-99';
        bVal = b.dataset.date || '9999-99-99';
        break;
      case 'budget':
        aVal = parseFloat(a.dataset.budget) || 0;
        bVal = parseFloat(b.dataset.budget) || 0;
        break;
      case 'spent':
        aVal = parseFloat(a.dataset.spent) || 0;
        bVal = parseFloat(b.dataset.spent) || 0;
        break;
      case 'status':
        aVal = a.dataset.status || '';
        bVal = b.dataset.status || '';
        break;
      case 'region':
        aVal = a.dataset.region || '';
        bVal = b.dataset.region || '';
        break;
      case 'sector':
        aVal = a.dataset.sector || '';
        bVal = b.dataset.sector || '';
        break;
      default:
        aVal = a.dataset.name || '';
        bVal = b.dataset.name || '';
    }
    
    let comparison = 0;
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      comparison = aVal - bVal;
    } else {
      comparison = String(aVal).localeCompare(String(bVal));
    }
    
    return sortOrder === 'desc' ? -comparison : comparison;
  });
  
  // Reorder DOM
  visibleCards.forEach(card => grid.appendChild(card));
  // Append hidden cards at the end
  cards.filter(card => card.style.display === 'none').forEach(card => grid.appendChild(card));
}

// Open edit modal
async function openEditModal(projectId) {
  currentProjectId = projectId;
  try {
    const response = await fetch(`/api/project/${projectId}`);
    const project = await response.json();
    
    // Populate regions first (before setting values)
    populateRegions();
    
    // Populate form with project data
    document.querySelector('input[name="name"]').value = project.name;
    document.querySelector('select[name="project_sector"]').value = project.project_sector;
    document.querySelector('select[name="region"]').value = project.region;
    document.querySelector('select[name="status"]').value = project.status;
    document.querySelector('input[name="allocated_budget"]').value = project.allocated_budget;
    document.querySelector('input[name="spent"]').value = project.spent;
    document.querySelector('textarea[name="description"]').value = project.description || '';
    
    // Show current image preview if exists
    const imagePreviewContainer = document.getElementById('currentImagePreview');
    const imagePreview = document.getElementById('editImagePreview');
    const uploadLabel = document.getElementById('editUploadLabel');
    const fileName = document.getElementById('editFileName');
    
    if (project.project_image) {
      imagePreview.src = '/static/' + project.project_image;
      fileName.textContent = project.project_image.split('/').pop();
      imagePreviewContainer.style.display = 'flex';
      uploadLabel.style.display = 'none';
    } else {
      imagePreviewContainer.style.display = 'none';
      uploadLabel.style.display = 'flex';
    }
    
    // Clear file input
    const fileInput = document.getElementById('editProjectImageInput');
    if (fileInput) fileInput.value = '';
    
    // Show modal
    document.getElementById('editModal').style.display = 'flex';
  } catch (error) {
    console.error('Error loading project:', error);
    alert('Error loading project data');
  }
}

// Clear edit file input and show upload label
function clearEditFileInput() {
  const input = document.getElementById('editProjectImageInput');
  const preview = document.getElementById('currentImagePreview');
  const uploadLabel = document.getElementById('editUploadLabel');
  
  input.value = '';
  preview.style.display = 'none';
  uploadLabel.style.display = 'flex';
}

// Close edit modal
function closeEditModal(event) {
  if (event && event.target !== document.getElementById('editModal')) return;
  document.getElementById('editModal').style.display = 'none';
  currentProjectId = null;
}

// Populate regions dropdown
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

// Handle edit form submit
async function handleEditFormSubmit(e) {
  e.preventDefault();
  
  showConfirmation('Are you sure you want to save the changes to this project?', async () => {
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
}

// Delete project function
function deleteProject() {
  if (!currentProjectId) return;
  
  showConfirmation('Are you sure you want to delete this project? This action cannot be undone.', async () => {
    try {
      const formData = new FormData();
      const response = await fetch(`/project/${currentProjectId}/delete`, {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        location.reload();
      } else {
        alert('Error deleting project');
      }
    } catch (error) {
      console.error('Error deleting project:', error);
      alert('Error deleting project');
    }
  });
}
