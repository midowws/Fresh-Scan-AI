import logging
import tensorflow as tf
from flask import Flask, render_template
from flask_cors import CORS
from backend.routes.predict import predict_bp

logging.basicConfig(level=logging.INFO)

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

CORS(app)
app.config.from_object('backend.config.Config')

app.register_blueprint(predict_bp)

path_model = app.config.get('MODEL_PATH')
try:
    if path_model:
        model = tf.keras.models.load_model(path_model)
        logging.info(f"Berhasil memuat model dari: {path_model}")
        app.config['MODEL'] = model
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

if __name__ == '__main__':
    app.run(debug=True)
