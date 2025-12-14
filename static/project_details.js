// project_details.js - Project details page functionality

// File upload preview functionality for project reports
document
  .getElementById("projectReportImageInput")
  .addEventListener("change", function (e) {
    const file = e.target.files[0];
    const preview = document.getElementById("projectReportFilePreview");
    const previewImage = document.getElementById("projectReportPreviewImage");
    const fileName = document.getElementById("projectReportFileName");
    const uploadLabel = document.querySelector(
      '[for="projectReportImageInput"].file-upload-label'
    );

    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        previewImage.src = e.target.result;
        fileName.textContent = file.name;
        preview.style.display = "flex";
        uploadLabel.style.display = "none";
      };
      reader.readAsDataURL(file);
    }
  });

function clearProjectReportFileInput() {
  const input = document.getElementById("projectReportImageInput");
  const preview = document.getElementById("projectReportFilePreview");
  const uploadLabel = document.querySelector(
    '[for="projectReportImageInput"].file-upload-label'
  );

  input.value = "";
  preview.style.display = "none";
  uploadLabel.style.display = "flex";
}
