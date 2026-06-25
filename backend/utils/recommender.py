import numpy as np
import logging

CLASS_NAMES = [
    'apple_fresh', 'apple_rotten',
    'banana_fresh', 'banana_rotten',
    'cucumber_fresh', 'cucumber_rotten',
    'okra_fresh', 'okra_rotten',
    'oranges_fresh', 'oranges_rotten',
    'tomato_fresh', 'tomato_rotten'
]

TRANSLATIONS = {
    'apple': 'Apel',
    'banana': 'Pisang',
    'cucumber': 'Mentimun',
    'okra': 'Okra',
    'oranges': 'Jeruk',
    'tomato': 'Tomat'
}


def analyze_prediction(prediction_array):
    try:
        class_idx = int(np.argmax(prediction_array[0]))
        if class_idx >= len(CLASS_NAMES):
            class_idx = len(CLASS_NAMES) - 1
        confidence = float(prediction_array[0][class_idx])

        raw_label = CLASS_NAMES[class_idx]

        parts = raw_label.split('_')
        tipe_inggris = parts[0]
        kondisi_inggris = parts[1]

        tipe_indo = TRANSLATIONS.get(tipe_inggris, tipe_inggris.title())

        if kondisi_inggris == 'fresh':
            kualitas = 'Segar'
            pesan = f"Bagus! {tipe_indo} ini masih dalam kondisi segar. Simpan di tempat sejuk atau lemari pendingin agar kesegarannya lebih tahan lama."
        else:
            kualitas = 'Tidak Segar'
            pesan = f"Perhatian: {tipe_indo} ini menunjukkan tanda pembusukan. Pisahkan segera dari bahan pangan lain agar jamur/bakterinya tidak menular."

        return {
            'tipe_item': tipe_indo,
            'kualitas': kualitas,
            'confidence': confidence,
            'pesan_rekomendasi': pesan
        }
    except Exception as e:
        logging.exception("Gagal menerjemahkan hasil prediksi di recommender.py")
        raise ValueError("Gagal membaca hasil klasifikasi multiclass.")
