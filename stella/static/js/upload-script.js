function updateFileName() {
      var fileInput = document.getElementById('file-input');
      var fileNameSpan = document.getElementById('file-name');
      fileNameSpan.textContent = fileInput.files[0] ? fileInput.files[0].name : 'No file chosen';
}
