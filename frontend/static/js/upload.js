const API_URL = "/predict";

const fileInput   = document.getElementById('fileInput');
const dropArea    = document.getElementById('dropArea');
const uploadText  = document.getElementById('uploadText');
const previewWrap = document.getElementById('previewWrap');
const previewImg  = document.getElementById('previewImg');
const openCameraBtn = document.getElementById('openCameraBtn');
const cameraPanel = document.getElementById('cameraPanel');
const cameraVideo = document.getElementById('cameraVideo');
const captureBtn = document.getElementById('captureBtn');
const closeCameraBtn = document.getElementById('closeCameraBtn');
const predictBtn  = document.getElementById('predictBtn');
const resetBtn    = document.getElementById('resetBtn');
const errorBox    = document.getElementById('errorBox');

let selectedFile = null;
let cameraStream = null;

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

function stopCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
  cameraVideo.srcObject = null;
}

function openCamera() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showError('Kamera tidak tersedia di perangkat ini.');
    return;
  }

  navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    .then(stream => {
      cameraStream = stream;
      cameraVideo.srcObject = stream;
      cameraPanel.style.display = 'block';
      openCameraBtn.disabled = true;
      clearError();
    })
    .catch(err => {
      console.error(err);
      showError('Gagal membuka kamera. Periksa izin dan perangkat kamera.');
    });
}

function capturePhoto() {
  if (!cameraVideo.srcObject) return;

  const canvas = document.createElement('canvas');
  canvas.width = cameraVideo.videoWidth;
  canvas.height = cameraVideo.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(cameraVideo, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    if (!blob) {
      showError('Gagal mengambil foto. Coba lagi.');
      return;
    }

    const file = new File([blob], 'camera-photo.png', { type: 'image/png' });
    handleFile(file);
    stopCamera();
    cameraPanel.style.display = 'none';
    openCameraBtn.disabled = false;
  }, 'image/png');
}

function resetUpload() {
  selectedFile = null;
  previewImg.src = '';
  previewWrap.style.display = 'none';
  uploadText.textContent = 'Klik atau seret gambar ke sini';
  predictBtn.disabled = true;
  fileInput.value = '';
  clearError();
  stopCamera();
  cameraPanel.style.display = 'none';
  openCameraBtn.disabled = false;
  if (typeof resetResult === 'function') resetResult();
}

openCameraBtn.addEventListener('click', openCamera);
captureBtn.addEventListener('click', capturePhoto);
closeCameraBtn.addEventListener('click', () => {
  stopCamera();
  cameraPanel.style.display = 'none';
  openCameraBtn.disabled = false;
});

resetBtn.addEventListener('click', resetUpload);

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
