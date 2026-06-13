const API_URL = "http://127.0.0.1:5000/predict";

const fileInput = document.getElementById('fileInput');
const dropArea = document.getElementById('dropArea');
const uploadText = document.getElementById('uploadText');
const previewWrap = document.getElementById('previewWrap');
const previewImg = document.getElementById('previewImg');
const predictBtn = document.getElementById('predictBtn');
const errorBox = document.getElementById('errorBox');

let selectedFile = null;

function showError(message) {
  errorBox.textContent = message;
  errorBox.style.display = 'block';
}

function clearError() {
  errorBox.style.display = 'none';
  errorBox.textContent = '';
}

function handleFile(file) {
  clearError();

  if (!file) return;

  if (!file.type.startsWith('image/')) {
    showError('File yang dipilih bukan gambar. Silakan pilih file JPG atau PNG.');
    return;
  }

  const maxSize = 5 * 1024 * 1024; // 5MB, sesuai config.py
  if (file.size > maxSize) {
    showError('Ukuran file terlalu besar. Maksimal 5MB.');
    return;
  }

  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewWrap.style.display = 'block';
    uploadText.textContent = file.name;
    predictBtn.disabled = false;
    if (typeof resetResult === 'function') resetResult();
  };
  reader.readAsDataURL(file);
}

fileInput.addEventListener('change', (e) => {
  handleFile(e.target.files[0]);
});

// Drag & drop
['dragenter', 'dragover'].forEach(evt => {
  dropArea.addEventListener(evt, (e) => {
    e.preventDefault();
    dropArea.classList.add('dragover');
  });
});

['dragleave', 'drop'].forEach(evt => {
  dropArea.addEventListener(evt, (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragover');
  });
});

dropArea.addEventListener('drop', (e) => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

// ---------- Kirim ke Backend Flask ----------
predictBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  clearError();
  predictBtn.disabled = true;
  predictBtn.textContent = 'Menganalisis...';

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || 'Terjadi kesalahan pada server.');
      if (typeof resetResult === 'function') resetResult();
      return;
    }

    if (typeof showResult === 'function') {
      showResult(data);
    }

  } catch (err) {
    console.error(err);
    showError('Gagal terhubung ke server. Pastikan backend (app.py) sedang berjalan.');
    if (typeof resetResult === 'function') resetResult();
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = 'Prediksi Kesegaran';
  }
});
