# Analisis Jejaring Sosial (Social Network Analysis)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bayubella/Analisis-Jejaring-Sosial/blob/main/Analisis_Jejaring_Sosial.ipynb)

Repositori ini berisi proyek analisis jejaring sosial menggunakan dataset riil **ego-Facebook** yang bersumber dari **Stanford Large Network Dataset Collection (SNAP)**. Proyek ini memetakan lingkaran pertemanan anonim di Facebook (4.039 node dan 88.234 edge) untuk mengevaluasi sentralitas aktor, deteksi komunitas, serta simulasi propagasi penyebaran informasi.

## 👤 Informasi Mahasiswa
- **Nama:** Bayu Samudra
- **NIM:** 2211310079
- **Kelas:** Teknologi Informasi 8c
- **Mata Kuliah:** Analisis Jejaring Sosial

---

## 💻 Pengodean dan Pengujian (Google Colab)

Seluruh proses analisis, pemodelan, simulasi, dan visualisasi interaktif dikemas di dalam file **Jupyter Notebook** yang dapat Anda jalankan langsung di Google Colab tanpa instalasi lokal.

Silakan klik tombol di bawah ini untuk membuka notebook di Google Colab:  
👉 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bayubella/Analisis-Jejaring-Sosial/blob/main/Analisis_Jejaring_Sosial.ipynb)

---

## 📁 Struktur File Repositori

- `Analisis_Jejaring_Sosial.ipynb`: Jupyter Notebook yang dirancang khusus untuk Google Colab (lengkap dengan penjelasan teks Markdown dan visualisasi).
- `analisis_sna.py`: Skrip program Python mandiri yang bersih (hasil konversi notebook).
- `LAPORAN.md`: Laporan akhir resmi dalam Bahasa Indonesia yang menjawab 5 pertanyaan penugasan dengan teori dan hasil perhitungan riil.
- `requirements.txt`: Daftar pustaka Python yang diperlukan untuk eksekusi lokal.

---

## 🛠️ Cara Menjalankan Secara Lokal

Jika Anda ingin menjalankan analisis ini di komputer lokal Anda:

### 1. Instalasi Pustaka
Pastikan Anda telah menginstal Python (>= 3.8), kemudian buka terminal dan jalankan:
```bash
pip install -r requirements.txt
```

### 2. Jalankan Program
Eksekusi file skrip utama untuk mengunduh dataset SNAP secara otomatis, menghitung metrik, menjalankan simulasi, serta menghasilkan berkas grafik:
```bash
python analisis_sna.py
```

### 3. Hasil Output Lokal
- `network_static.png`: Visualisasi statis graf pertemanan Facebook dengan pewarnaan berdasarkan 16 komunitas Louvain.
- `simulation_plot.png`: Grafik kurva pertumbuhan penyebaran informasi model SI.
- `network_interactive.html`: File visualisasi web interaktif berbasis HTML. Buka file ini di Google Chrome, Firefox, atau Edge Anda untuk menjelajahi jejaring secara interaktif.
