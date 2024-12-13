# Dokumentasi PanenCerdas

## 🚀 Cara Menjalankan Proyek

**Clone repositori**:
   ```bash
   git clone https://github.com/username/panen-cerdas.git
   cd panen-cerdas
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```
   Akses aplikasi di http://127.0.0.1:5000.


## 📂 Struktur Projek

```plaintext
PANEN-CERDAS/
│
├── helper/                          # Folder untuk fungsi-fungsi pendukung logika aplikasi
│   ├── __pycache__/                 # Folder cache Python (otomatis)
│   ├── ClimateVisualization.py      # Fungsi Untuk Menghasilkan Visualisasi data iklim
│   ├── historicalDataComparison.py  # Fungsi untuk Menghasilkan Visualisasi Perbandingan data historis
│   ├── ohe.pkl                      # Model One-Hot Encoding yang telah disimpan
│   ├── scatterPlotBetweenFeature.py # Fungsi untuk Menghasilkan Visualisasi Scatter plot antar fitur
│   ├── summaryByProvince.py         # Fungsi untuk Menghasilkan Ringkasan data berdasarkan provinsi
│   ├── totalHarvestByProvince.py    # Fungsi untuk Menghasilkan Visualisasi Total hasil panen per provinsi
│   ├── totalHarvestEachProvince.py  # Fungsi untuk Menghasilkan Visualisasi Total hasil panen setiap provinsi
│
├── static/                        # Folder untuk file statis (CSS, JS, Images)
│   ├── css/                       # Folder untuk file CSS
│   │   └── styles.css             # File css untuk tampilan website
│   ├── images/                    # Folder untuk gambar
│   ├── js/                        # Folder untuk file JavaScript
│       └── scripts.js             # Script JavaScript untuk interaksi website seperti memproses ketika tombol ditekan
└── savefig/                       # Folder untuk menyimpan grafik hasil plot
    └── barchart_each_provinsi_based_on_tahun.png    # Grafik bar chart per provinsi berdasarkan tahun
    └── hasil_panen_per_tahun_provinsi.png           # Grafik hasil panen per tahun per provinsi
    └── line_plot_data_iklim_provinsi_x.png          # Grafik line plot data iklim per provinsi
    └── prediksi_produksi_padi.png                   # Grafik prediksi produksi padi
    └── scatter_plot_fitur_a_dengan_b_provinsi_x.png # Grafik scatter plot antara fitur A dan B per provinsi
│
├── templates/                     # Folder untuk template HTML
│   ├── dashboard.html             # Template halaman dashboard
│   ├── hasil.html                 # Template untuk hasil analisis
│   ├── index.html                 # Template halaman utama
│   ├── prediksi.html              # Template untuk prediksi data
│
├── venv/                          # Virtual environment untuk proyek
│
├── .gitignore                     # File untuk mengabaikan file tertentu di Git
├── app.py                         # Entry point aplikasi Flask
├── requirements.txt               # Daftar dependensi Python
```

## 📖 Penjelasan Folder dan File

- **`helper/`**  
  Berisi modul Python dengan fungsi-fungsi pendukung seperti visualisasi data, analisis perbandingan, dan pengolahan hasil panen.

- **`static/`**  
  Berisi file statis seperti CSS, JavaScript, dan grafik yang disimpan. Folder ini membantu mendukung tampilan frontend.

- **`templates/`**  
  Berisi template HTML untuk halaman web yang dirender oleh Flask.

- **`venv/`**  
  Virtual environment untuk mengisolasi dependensi Python proyek.

- **`app.py`**  
  File utama yang menjalankan aplikasi Flask.

- **`requirements.txt`**  
  Berisi daftar dependensi Python untuk proyek. Instal dependensi ini dengan:
  ```bash
  pip install -r requirements.txt
