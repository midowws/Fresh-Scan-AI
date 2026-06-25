let resultEmpty, resultContent, resultStatus, statusIcon, statusText, confidenceValue, confidenceFill, recommendationText, detailType, detailQuality, detailTime;

document.addEventListener('DOMContentLoaded', function() {
  resultEmpty = document.getElementById('resultEmpty');
  resultContent = document.getElementById('resultContent');
  resultStatus = document.getElementById('resultStatus');
  statusIcon = document.getElementById('statusIcon');
  statusText = document.getElementById('statusText');
  confidenceValue = document.getElementById('confidenceValue');
  confidenceFill = document.getElementById('confidenceFill');
  recommendationText = document.getElementById('recommendationText');
  detailType = document.getElementById('detailType');
  detailQuality = document.getElementById('detailQuality');
  detailTime = document.getElementById('detailTime');
});

function resetResult() {
  if (!resultEmpty || !resultContent) return;
  resultEmpty.style.display = 'flex';
  resultContent.style.display = 'none';
  confidenceFill.style.width = '0%';
  resultStatus.classList.remove('unfresh', 'unsure');
}

function showResult(data) {
  if (!resultEmpty || !confidenceFill) return;
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
