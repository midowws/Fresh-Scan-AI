import logging
import numpy as np
import cv2
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')

model = None
try:
    path_model = app.config['MODEL_PATH']
    model = tf.keras.models.load_model(path_model)
    logging.info(f"Berhasil memuat model dari: {path_model}")
except Exception as e:
    logging.exception(f"Gagal memuat model dari {path_model}: {e}")

kategori = ['Segar', 'Tidak Segar'] 

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({'error': 'Model tidak tersedia di server'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nama file tidak boleh kosong'}), 400

    ekstensi = file.filename.split('.')[-1].lower()
    if ekstensi not in app.config['ALLOWED_EXTENSIONS']:
        return jsonify({'error': 'Format file tidak didukung'}), 400

    try:
        file_data = file.read()
        npimg = np.frombuffer(file_data, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Gagal membaca gambar, file mungkin rusak'}), 400

        # --- PREPROCESSING YANG BENAR ---
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img) # Mengubah rentang pixel sesuai MobileNetV2
        
    except Exception as e:
        logging.exception('Image preprocessing failed')
        return jsonify({'error': f'Gagal memproses gambar secara matematis: {str(e)}'}), 400

    try:
        prediction = model.predict(img)
        
        # --- LOGIKA KLASIFIKASI BINER (SIGMOID) ---
        # prediction menghasilkan array seperti [[0.85]]
        score = prediction[0][0]
        
        # Mapping kelas: 'fresh': 0, 'rotten': 1 (Sesuai train.py)
        if score >= 0.5:
            predict_class = 1 # Tidak Segar
            confidence_score = float(score) 
        else:
            predict_class = 0 # Segar
            confidence_score = float(1.0 - score) 
            
        if confidence_score < 0.70:
            return jsonify({
                'prediction': 'Tidak Yakin, mohon foto ulang', 
                'confidence': confidence_score
            })
        
        hasil = kategori[predict_class]
        return jsonify({
            'prediction': hasil, 
            'confidence': confidence_score
        })
        
    except Exception as e:
        logging.exception('Prediction execution failed')
        return jsonify({'error': f'Terjadi kegagalan saat menjalankan prediksi: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
