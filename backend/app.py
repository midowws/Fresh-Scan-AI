import logging
import numpy as np
import cv2
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.preprocessor import prepare_image
from utils.recommender import analyze_prediction
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

CORS(app)
app.config.from_object('config.Config')

model = None
path_model = app.config.get('MODEL_PATH')
try:
    if path_model:
        model = tf.keras.models.load_model(path_model)
        logging.info(f"Berhasil memuat model dari: {path_model}")
    else:
        logging.warning('MODEL_PATH not configured; model not loaded.')
except Exception as e:
    logging.exception(f"Gagal memuat model dari {path_model}: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/classify')
def classify():
    return render_template('classify.html')

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({'error': 'Model tidak tersedia di server'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nama file tidak boleh kosong'}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({'error': 'Nama file tidak valid'}), 400

    if '.' not in filename:
        return jsonify({'error': 'Nama file tidak memiliki ekstensi'}), 400

    ekstensi = filename.rsplit('.', 1)[1].lower()
    allowed = app.config.get('ALLOWED_EXTENSIONS', [])
    if ekstensi not in allowed:
        return jsonify({'error': 'Format file tidak didukung'}), 400

    try:
        file_data = file.read()
        img = prepare_image(file_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    try:
        prediction = model.predict(img)
        
        #ppakai llogic recomencer baru
        hasil_analisis = analyze_prediction(prediction)
        
        confidence_score = hasil_analisis['confidence']
        
        if confidence_score < 0.60:
            return jsonify({
                'prediction': 'Tidak Yakin, mohon foto ulang', 
                'confidence': round(confidence_score, 2),
                'pesan': 'Sistem kurang yakin. Mohon foto ulang dengan pencahayaan dan fokus yang lebih baik.',
                'tipe': 'Tidak Diketahui'
            }), 200
        
        return jsonify({
            'prediction': hasil_analisis['kualitas'], 
            'confidence': round(confidence_score, 2),
            'pesan': hasil_analisis['pesan_rekomendasi'],
            'tipe': hasil_analisis['tipe_item']
        }), 200
        
    except Exception as e:
        logging.exception('Prediction execution failed')
        return jsonify({'error': f'Terjadi kegagalan saat menjalankan prediksi: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
