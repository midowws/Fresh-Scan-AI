# Fresh-Scan-AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)]()
[![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask&logoColor=white)]()

**Fresh-Scan-AI** merupakan sistem terintegrasi berbasis *Artificial Intelligence* (AI) yang dikembangkan untuk mengevaluasi dan mengklasifikasikan tingkat kesegaran bahan pangan (seperti daging, sayuran, dan buah-buahan) melalui analisis citra visual. Proyek ini diinisiasi sebagai solusi teknologi untuk menekan tingkat pemborosan makanan (*food waste*) sekaligus memberikan panduan protokol penyimpanan pangan yang optimal.

---

## 🌐 Live Deployment

Sistem ini telah dikerahkan ke tahap produksi dan dapat diakses untuk pengujian publik melalui tautan berikut:

🔗 **[Fresh-Scan-AI Live Environment](https://activist-underhand-clutter.ngrok-free.dev)**

*(Catatan: Lingkungan deployment ini menggunakan tunneling via ngrok. Tautan dapat berubah bergantung pada siklus pemeliharaan server).*

---

## 🚀 Kapabilitas & Fitur Utama

* **Analisis Kesegaran Real-Time:** Mengimplementasikan model AI untuk memproses citra bahan pangan dan menghasilkan metrik klasifikasi kesegaran dengan tingkat akurasi tinggi.
* **Sistem Rekomendasi Penyimpanan (Storage Protocol):** Mengembalikan data komprehensif mengenai estimasi *shelf-life* (umur simpan) berdasarkan kondisi lingkungan, seperti suhu ruang, refrigerasi, atau metode *vacuum sealing*.
* **Antarmuka Intuitif (Seamless UI/UX):** Menyediakan *dashboard* interaktif yang memungkinkan pengguna untuk mengunggah atau memotret sampel secara langsung dari perangkat dengan antarmuka yang responsif.
* **Skalabilitas Arsitektur:** Struktur kode dirancang secara modular agar mudah diintegrasikan dengan API eksternal atau basis data di masa mendatang.

---

## 🛠️ Arsitektur & Teknologi

Sistem ini dibangun dengan mengadopsi pendekatan *full-stack*, memanfaatkan teknologi berikut untuk memastikan performa yang stabil dan efisien:

* **Backend Environment:** Python, Flask 
* **Frontend Interface:** HTML5, CSS3, Vanilla JavaScript
* **AI & Computer Vision:** Integrasi Model Large Language/Vision (AI API)
* **Deployment & Tunneling:** Ngrok, Vercel

---

## 📂 Struktur Direktori Proyek

Dokumentasi arsitektur direktori utama dalam repositori ini disusun sebagai berikut:

```text
Fresh-Scan-AI/
├── static/             # Aset antarmuka statis (CSS, JS, Media)
├── templates/          # Komponen User Interface (File HTML)
├── models/             # Konfigurasi atau penyimpanan model AI terkait
├── app.py              # Titik masuk utama logika aplikasi backend
├── requirements.txt    # Manifes dependensi dan pustaka sistem
└── README.md           # Dokumentasi utama proyek


```
                                              /===-_---~~~~~~~~~------____
                                             |===-~___                _,-'
                  -==\\                         `//~\\   ~~~~`---.___.-~~
              ______-==|                         | |  \\           _-~`
        __--~~~  ,-/-==\\                        | |   `\        ,'
     _-~       /'    |  \\                      / /      \      /
   .'        /       |   \\                   /' /        \   /'
  /  ____  /         |    \`\.__/-~~ ~ \ _ _/'  /          \/'
 /-'~    ~~~~~---__  |     ~-/~         ( )   /'
                   \_|      /        _) | ;  ),   __--~~
                     '~~--_/      _-~/- |/ \   '-~ \
                    {\__--_/}    / \\_>-|)<__\      \
                    /'   (_/  _-~  | |__>--<__|      |
                   |   _/) )-~     | |__>--<__|      |
                   / /~ ,_/       / /__>---<__/      |
                  o-o _//        /-~_>---<__-~      /
                  (^(~          /~_>---<__-      _-~
                 ,/|           /__>--<__/     _-~
              ,//('(          |__>--<__|     /                 
             ( ( '))          |__>--<__|    |
          `-)) )) (           |__>--<__|    |
         ,/,'//( (            \__>--<__/    |
       ,( ( ((, ))             ~-__>--<_~-_/
     `~/  )` ) ,/|                 ~-_~>--<_/
   ._-~//( )/ )) `                    ~~-' 
    ;'( ')/ ,)(                             
   ' ') '( (/                              
     '   '  `
```
