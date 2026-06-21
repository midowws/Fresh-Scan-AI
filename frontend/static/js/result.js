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

const recommendations = {
  fresh: [
    "Simpan pada suhu 4-7°C dalam wadah berventilasi untuk menjaga kesegaran lebih lama. Hindari menyimpan bersama produk yang menghasilkan gas etilen tinggi seperti pisang matang.",
    "Bahan pangan dalam kondisi segar. Sebaiknya segera digunakan dalam 2-4 hari atau simpan di lemari pendingin dengan kelembaban terjaga untuk hasil optimal."
  ],
  unfresh: [
    "Produk menunjukkan tanda penurunan kualitas. Sebaiknya tidak dikonsumsi mentah, periksa bagian yang membusuk dan segera olah atau buang bagian tersebut.",
    "Tingkat kesegaran rendah terdeteksi. Disarankan untuk segera memeriksa secara fisik, memisahkan dari bahan pangan lain, dan tidak menyimpannya lebih lama."
  ],
  unsure: [
    "Sistem belum cukup yakin dengan hasil klasifikasi ini. Coba ambil ulang foto dengan pencahayaan yang lebih baik dan fokus pada satu jenis bahan pangan."
  ]
};

function resetResult() {
  resultEmpty.style.display = 'flex';
  resultContent.style.display = 'none';
  confidenceFill.style.width = '0%';
  resultStatus.classList.remove('unfresh', 'unsure');
}

// data = { prediction: string, confidence: number(0-1) }
function showResult(data) {
  const prediction = data.prediction;
  const confidence = (data.confidence * 100).toFixed(1);

  resultEmpty.style.display = 'none';
  resultContent.style.display = 'block';

  resultStatus.classList.remove('unfresh', 'unsure');

  let recArr;

  if (prediction === 'Segar') {
    statusIcon.textContent = '✅';
    statusText.textContent = 'Segar';
    detailQuality.textContent = 'Baik';
    recArr = recommendations.fresh;
  } else if (prediction === 'Tidak Segar') {
    statusIcon.textContent = '⚠️';
    statusText.textContent = 'Tidak Segar';
    detailQuality.textContent = 'Menurun';
    resultStatus.classList.add('unfresh');
    recArr = recommendations.unfresh;
  } else {
    // "Tidak Yakin, mohon foto ulang" atau prediksi lain yang tidak dikenali
    statusIcon.textContent = '❓';
    statusText.textContent = prediction;
    detailQuality.textContent = '—';
    resultStatus.classList.add('unsure');
    recArr = recommendations.unsure;
  }

  confidenceValue.textContent = `${confidence}%`;
  requestAnimationFrame(() => {
    confidenceFill.style.width = `${confidence}%`;
  });

  recommendationText.textContent = recArr[Math.floor(Math.random() * recArr.length)];

  detailType.textContent = 'Buah / Sayur';
  detailTime.textContent = new Date().toLocaleTimeString('id-ID');
}
