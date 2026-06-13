import os
import logging
import numpy as np
import cv2
import tensorflow as tf
from flask import Flask, request

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Make model path configurable via environment variable
MODEL_PATH = os.environ.get('MODEL_PATH', 'path/to/your/model.h5')
model = None
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    logging.info(f"Loaded model from {MODEL_PATH}")
except Exception as e:
    logging.exception(f"Failed to load model from {MODEL_PATH}: {e}")

kategori = ['Segar', 'Busuk']


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return {'error': 'Model tidak tersedia'}, 500

    if 'file' not in request.files:
        return {'error': 'Tidak ada file yang diunggah'}, 400

    file = request.files['file']

    if file.filename == '':
        return {'error': 'Nama file tidak boleh kosong'}, 400

    if file.filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png']:
        return {'error': 'Format file tidak didukung'}, 400

    file_data = file.read()
    npimg = np.frombuffer(file_data, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if img is None:
        return {'error': 'Gagal membaca gambar'}, 400

    try:
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
    except Exception as e:
        logging.exception('Image preprocessing failed')
        return {'error': f'Gagal memproses gambar: {str(e)}'}, 400

    try:
        prediction = model.predict(img)
        predict_class = int(np.argmax(prediction, axis=1)[0])
        confidence_score = np.max(prediction)
        if confidence_score < 0.70:
            return {'prediction': 'Tidak Yakin, mohon foto ulang', 'confidence': float(confidence_score)}
        hasil = kategori[predict_class]
        return {'prediction': hasil, 'confidence': float(confidence_score)}
    except Exception as e:
        logging.exception('Prediction failed')
        return {'error': f'Gagal menjalankan prediksi: {str(e)}'}, 500


if __name__ == '__main__':
    app.run(debug=True)
