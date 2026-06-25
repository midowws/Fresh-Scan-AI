from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from backend.utils.preprocessor import prepare_image
from backend.utils.recommender import analyze_prediction

predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/predict', methods=['POST'])
def predict():
    model = current_app.config.get('MODEL')
    if model is None:
        return jsonify({'error': 'Model tidak tersedia di server'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

    filename = secure_filename(file.filename)
    if not filename or '.' not in filename:
        return jsonify({'error': 'Nama file tidak valid atau tidak memiliki ekstensi'}), 400

    ekstensi = filename.rsplit('.', 1)[1].lower()
    if ekstensi not in current_app.config.get('ALLOWED_EXTENSIONS', set()):
        return jsonify({'error': 'Format file tidak didukung'}), 400

    try:
        img = prepare_image(file.read())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    try:
        prediction = model.predict(img)
        hasil_analisis = analyze_prediction(prediction)
        confidence = hasil_analisis['confidence']

        if confidence < 0.60:
            return jsonify({
                'prediction': 'Tidak Yakin, mohon foto ulang',
                'confidence': round(confidence, 2),
                'pesan': 'Sistem kurang yakin. Mohon foto ulang dengan pencahayaan dan fokus yang lebih baik.',
                'tipe': 'Tidak Diketahui'
            }), 200

        return jsonify({
            'prediction': hasil_analisis['kualitas'],
            'confidence': round(confidence, 2),
            'pesan': hasil_analisis['pesan_rekomendasi'],
            'tipe': hasil_analisis['tipe_item']
        }), 200

    except Exception as e:
        current_app.logger.exception('Prediction failed')
        return jsonify({'error': f'Terjadi kegagalan saat menjalankan prediksi: {str(e)}'}), 500