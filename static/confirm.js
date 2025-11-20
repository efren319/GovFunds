// confirm.js - Handle confirmation dialogs for critical actions

/**
 * Show a custom confirmation dialog
 * @param {string} message - The confirmation message
 * @param {function} onConfirm - Callback when user confirms
 * @param {function} onCancel - Callback when user cancels (optional)
 */
function showConfirmation(message, onConfirm, onCancel) {
  const dialog = document.createElement('div');
  dialog.className = 'confirmation-dialog-overlay';
  
  const dialogContent = document.createElement('div');
  dialogContent.className = 'confirmation-dialog';
  
  dialogContent.innerHTML = `
    <div class="confirmation-dialog-header">
      <h3>Confirm Action</h3>
    </div>
    <div class="confirmation-dialog-body">
      <p>${message}</p>
    </div>
    <div class="confirmation-dialog-footer">
      <button class="btn-confirm">Yes, Confirm</button>
      <button class="btn-cancel">Cancel</button>
    </div>
  `;
  
  dialog.appendChild(dialogContent);
  document.body.appendChild(dialog);
  
  const confirmBtn = dialogContent.querySelector('.btn-confirm');
  const cancelBtn = dialogContent.querySelector('.btn-cancel');
  
  confirmBtn.addEventListener('click', () => {
    dialog.remove();
    if (onConfirm) onConfirm();
  });
  
  cancelBtn.addEventListener('click', () => {
    dialog.remove();
    if (onCancel) onCancel();
  });
  
  // Close on overlay click
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) {
      dialog.remove();
      if (onCancel) onCancel();
    }
  });
}

/**
 * Intercept form submissions and show confirmation
 */
document.addEventListener('DOMContentLoaded', () => {
  // Auto-remove flash messages after fade animation completes
  const flashMessages = document.querySelectorAll('.flash-list .flash');
  flashMessages.forEach(flash => {
    setTimeout(() => {
      flash.remove();
    }, 5000); // Remove after 5 seconds (matching animation duration)
  });

  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    // Skip forms that shouldn't have confirmation (like search forms)
    if (form.classList.contains('no-confirm')) return;
    
    form.addEventListener('submit', (e) => {
      // If form is already confirmed, let it submit
      if (form.dataset.confirmed === 'true') {
        form.dataset.confirmed = 'false';
        return;
      }
      
      e.preventDefault();
      
      let message = 'Are you sure you want to proceed with this action?';
      
      // Customize message based on form action
      const submitBtn = form.querySelector('button[type="submit"]');
      const btnText = submitBtn?.textContent.toLowerCase() || '';
      
      if (btnText.includes('save')) {
        message = 'Are you sure you want to save these changes?';
      } else if (btnText.includes('add')) {
        message = 'Are you sure you want to add this project?';
      } else if (btnText.includes('submit')) {
        message = 'Are you sure you want to submit this report?';
      } else if (btnText.includes('resolved')) {
        message = 'Are you sure you want to mark this as resolved?';
      }
      
      showConfirmation(message, () => {
        form.dataset.confirmed = 'true';
        form.submit();
      });
    });
  });
});
