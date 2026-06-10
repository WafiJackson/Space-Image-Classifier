# 🌌 Space Image Classifier

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**Aplikasi klasifikasi gambar luar angkasa menggunakan Deep Learning (CNN)**

Unggah gambar benda langit dan biarkan AI mengidentifikasinya dalam hitungan detik.

</div>

---

## 📋 Deskripsi

**Space Image Classifier** adalah aplikasi web berbasis _deep learning_ yang mampu mengklasifikasikan gambar objek luar angkasa ke dalam **6 kategori** secara otomatis. Proyek ini merupakan tugas **UAS Praktikum Machine Learning Semester 6 (2026)**.

Aplikasi ini menggunakan arsitektur **Convolutional Neural Network (CNN)** yang telah dilatih pada dataset _Space Image_ dan diintegrasikan dalam sebuah pipeline end-to-end: mulai dari upload gambar oleh pengguna melalui antarmuka **Streamlit**, pemrosesan dan prediksi oleh API **FastAPI**, hingga menampilkan hasil klasifikasi secara visual.

---

## 🪐 Kategori yang Didukung

| # | Kategori | Emoji | Deskripsi |
|---|----------|-------|-----------|
| 1 | **Constellation** | ✨ | Pola bintang yang membentuk rasi di langit malam |
| 2 | **Cosmos Space** | 🌀 | Pemandangan luas dari ruang angkasa kosmik |
| 3 | **Galaxies** | 🌌 | Kumpulan bintang, gas, dan debu yang terikat gravitasi |
| 4 | **Nebula** | 🔮 | Awan gas dan debu antarbintang yang bercahaya |
| 5 | **Planets** | 🪐 | Benda langit yang mengorbit bintang |
| 6 | **Stars** | ⭐ | Bola plasma raksasa yang memancarkan cahaya |

---

## ⚙️ Tech Stack

| Komponen | Teknologi | Keterangan |
|----------|-----------|------------|
| **Model ML** | TensorFlow / Keras | CNN untuk klasifikasi gambar (input 150×150 px) |
| **Backend API** | FastAPI + Uvicorn | REST API endpoint `/predict/` untuk inferensi model |
| **Frontend** | Streamlit | Antarmuka pengguna interaktif dengan tema premium _space_ |
| **Image Processing** | Pillow, NumPy | Preprocessing gambar sebelum prediksi |

---

## 📁 Struktur Proyek

```
Space-Image-Classifier/
│
├── backend/
│   ├── main.py                  # API FastAPI — endpoint prediksi
│   └── model/
│       ├── model_1_klasifikasi.h5   # Model CNN utama (best model)
│       └── model_2_klasifikasi.h5   # Model CNN alternatif
│
├── frontend/
│   └── app.py                   # Aplikasi Streamlit — UI pengguna
│
├── requirements.txt             # Daftar dependensi Python
├── .gitignore
└── Readme.md
```

---

## 🚀 Cara Menjalankan

### Prasyarat

- **Python 3.10+** sudah terinstall
- Koneksi internet (untuk install dependensi)

### 1. Clone Repository

```bash
git clone https://github.com/<username>/Space-Image-Classifier.git
cd Space-Image-Classifier
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

**Aktivasi:**

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Backend (FastAPI)

Buka terminal pertama:

```bash
uvicorn backend.main:app --reload --port 8000
```

Pastikan server berjalan di `http://127.0.0.1:8000`.

### 5. Jalankan Frontend (Streamlit)

Buka terminal kedua:

```bash
streamlit run frontend/app.py
```

Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`.

---

## 🎯 Cara Penggunaan

1. **Buka aplikasi** di browser setelah menjalankan backend dan frontend.
2. **Unggah gambar** benda langit (format: JPG, JPEG, atau PNG) melalui area upload.
3. **Klik tombol** "🚀 Klasifikasikan Sekarang".
4. **Lihat hasil** klasifikasi berupa:
   - Label kategori yang terdeteksi
   - Confidence score (tingkat keyakinan model)
   - Tingkat keyakinan: Tinggi (≥80%), Sedang (≥50%), atau Rendah (<50%)

---

## 🔗 API Endpoint

### `POST /predict/`

Mengirim gambar untuk diprediksi oleh model CNN.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` — file gambar (JPG/JPEG/PNG)

**Response:**
```json
{
  "label": "galaxies",
  "confidence": 0.9742
}
```

| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `label` | string | Nama kategori yang diprediksi |
| `confidence` | float | Skor kepercayaan (0.0 – 1.0) |

---

## 📦 Dependencies

```
fastapi==0.111.0
uvicorn==0.30.1
python-multipart==0.0.9
streamlit==1.35.0
tensorflow==2.16.1
Pillow==10.3.0
numpy==1.26.4
requests==2.32.3
h5py==3.11.0
```

---

## 🛠️ Alur Kerja Sistem

```
┌─────────────┐     HTTP POST      ┌─────────────────┐     Predict      ┌──────────────┐
│  Streamlit   │ ─────────────────▶ │   FastAPI API    │ ───────────────▶ │  CNN Model   │
│  (Frontend)  │ ◀───────────────── │   (Backend)      │ ◀─────────────── │  (TensorFlow)│
│  Port: 8501  │   JSON Response    │   Port: 8000     │   Prediction     │  150×150 px  │
└─────────────┘                     └─────────────────┘                   └──────────────┘
```

1. Pengguna mengunggah gambar melalui antarmuka **Streamlit**.
2. Gambar dikirim ke **FastAPI** via `POST /predict/`.
3. Backend melakukan **preprocessing** (resize ke 150×150, normalisasi 0–1).
4. Model **CNN** melakukan inferensi dan mengembalikan prediksi.
5. Hasil ditampilkan kembali di frontend dengan visualisasi confidence bar.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik — **UAS Praktikum Machine Learning, Semester 6 (2026)**.

---

<div align="center">

**Built with ❤️ using Streamlit & TensorFlow**

*Space Image Classifier v1.0*

</div>
