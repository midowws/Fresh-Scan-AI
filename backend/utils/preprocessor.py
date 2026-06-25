import cv2
import numpy as np
import logging
import tensorflow as tf


def prepare_image(file_data):
    npimg = np.frombuffer(file_data, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Gagal membaca gambar. File mungkin rusak.")

    try:
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32)
        img = np.expand_dims(img, axis=0)
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        return img
    except Exception as e:
        logging.exception('Image preprocessing failed di preprocessor.py')
        raise ValueError(f"Gagal memproses gambar: {str(e)}")
