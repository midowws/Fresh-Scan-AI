const API_URL = "/predict";

const fileInput   = document.getElementById('fileInput');
const dropArea    = document.getElementById('dropArea');
const uploadText  = document.getElementById('uploadText');
const previewWrap = document.getElementById('previewWrap');
const previewImg  = document.getElementById('previewImg');
const predictBtn  = document.getElementById('predictBtn');
const resetBtn    = document.getElementById('resetBtn');
const errorBox    = document.getElementById('errorBox');

let selectedFile = null;

function showError(message) {
  errorBox.textContent = message;
  errorBox.style.display = 'block';
}

function clearError() {
  errorBox.style.display = 'none';
  errorBox.textContent = '';
}

function resetAll() {
  selectedFile = null;
  fileInput.value = '';
  previewWrap.style.display = 'none';
  previewImg.src = '';
  uploadText.textContent = '📁 Pilih file atau seret ke sini';
  predictBtn.disabled = true;
  clearError();
  if (typeof resetResult === 'function') resetResult();
}

function handleFile(file) {
  clearError();
  if (!file) return;

  if (!['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)) {
    showError('Format tidak didukung. Gunakan file JPG atau PNG.');
    return;
  }

  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) {
    showError('Ukuran file terlalu besar. Maksimal 5MB.');
    return;
  }

  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewWrap.style.display = 'block';
    uploadText.textContent = '✅ ' + file.name;
    predictBtn.disabled = false;
    if (typeof resetResult === 'function') resetResult();
  };
  reader.readAsDataURL(file);
}

fileInput.addEventListener('change', (e) => {
  handleFile(e.target.files[0]);
});

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

resetBtn.addEventListener('click', () => resetAll());

predictBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  clearError();
  predictBtn.disabled = true;
  predictBtn.textContent = 'Menganalisis...';
  previewImg.classList.add('analyzing');

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

    if (typeof showResult === 'function') showResult(data);

  } catch (err) {
    console.error('Fetch error:', err);
    showError('Gagal terhubung ke server. Pastikan backend (app.py) sedang berjalan.');
    if (typeof resetResult === 'function') resetResult();
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = 'Unggah & Analisis';
    previewImg.classList.remove('analyzing');
  }
});
