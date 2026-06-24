const resultEmpty = document.getElementById('resultEmpty');
const resultContent = document.getElementById('resultContent');
const resultStatus = document.getElementById('resultStatus');
const statusIcon = document.getElementById('statusIcon');
const statusText = document.getElementById('statusText');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceFill = document.getElementById('confidenceFill');
const recommendationText = document.getElementById('recommendationText');
const detailType = document.getElementById('detailType');
const detailQuality = document.getElementById('detailQuality');
const detailTime = document.getElementById('detailTime');

function resetResult() {
  resultEmpty.style.display = 'flex';
  resultContent.style.display = 'none';
  confidenceFill.style.width = '0%';
  resultStatus.classList.remove('unfresh', 'unsure');
}

function showResult(data) {
  const prediction = data.prediction;
  const confidence = (data.confidence * 100).toFixed(1);

  resultEmpty.style.display = 'none';
  resultContent.style.display = 'block';

  resultStatus.classList.remove('unfresh', 'unsure');

  if (prediction === 'Segar') {
    statusIcon.textContent = '✅';
    statusText.textContent = 'Segar';
    detailQuality.textContent = 'Baik';
  } else if (prediction === 'Tidak Segar') {
    statusIcon.textContent = '⚠️';
    statusText.textContent = 'Tidak Segar';
    detailQuality.textContent = 'Menurun';
    resultStatus.classList.add('unfresh');
  } else {
    statusIcon.textContent = '❓';
    statusText.textContent = prediction;
    detailQuality.textContent = '—';
    resultStatus.classList.add('unsure');
  }

  confidenceValue.textContent = `${confidence}%`;
  requestAnimationFrame(() => {
    confidenceFill.style.width = `${confidence}%`;
  });

  // MENGAMBIL DATA DARI APP.PY
  recommendationText.textContent = data.pesan || "Tidak ada rekomendasi spesifik.";
  detailType.textContent = data.tipe || "Tidak Diketahui";
  detailTime.textContent = new Date().toLocaleTimeString('id-ID');
}
