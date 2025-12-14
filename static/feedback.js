// File upload preview functionality for report images
document
  .getElementById("reportImageInput")
  .addEventListener("change", function (e) {
    const file = e.target.files[0];
    const preview = document.getElementById("reportFilePreview");
    const previewImage = document.getElementById("reportPreviewImage");
    const fileName = document.getElementById("reportFileName");
    const uploadLabel = document.querySelector(
      '[for="reportImageInput"].file-upload-label'
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

function clearReportFileInput() {
  const input = document.getElementById("reportImageInput");
  const preview = document.getElementById("reportFilePreview");
  const uploadLabel = document.querySelector(
    '[for="reportImageInput"].file-upload-label'
  );

  input.value = "";
  preview.style.display = "none";
  uploadLabel.style.display = "flex";
}
