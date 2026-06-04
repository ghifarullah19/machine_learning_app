# Machine Learning Demo App

Aplikasi ini berisi demo sederhana untuk tiga studi kasus machine learning:

- Regresi: prediksi konsumsi minyak pemanas
- Klasifikasi: prediksi adopsi tablet
- Klasterisasi: segmentasi pelanggan

Proyek ini menyediakan dua cara menjalankan aplikasi:

- Flask API dan halaman web utama melalui `app.py`
- Streamlit dashboard melalui `streamlit_app.py`

Kalau file model belum tersedia, aplikasi tetap bisa berjalan dengan hasil simulasi bawaan.

## Fitur

- Prediksi regresi dari parameter rumah
- Prediksi klasifikasi dari profil pelanggan
- Segmentasi pelanggan ke dalam klaster
- Tampilan web sederhana untuk demo dan presentasi

## Struktur Folder

```text
.
├── app.py
├── streamlit_app.py
├── README.md
├── data/
│   └── processed_data.csv
├── models/
├── templates/
│   └── index.html
└── colab/
	├── tutorial_colab_clustering.ipynb
	├── tutorial_colab_klasifikasi.ipynb
	└── tutorial_colab_regresi.ipynb
```

## Kebutuhan

- Python 3.10 atau lebih baru
- pip
- Browser modern seperti Chrome, Edge, atau Safari

## Instalasi

### Windows

1. Buka PowerShell atau Command Prompt.
2. Masuk ke folder project.

```powershell
cd C:\Users\ghifa\Documents\machine-learning\code
```

3. Buat virtual environment.

```powershell
python -m venv .venv
```

4. Aktifkan virtual environment.

```powershell
.venv\Scripts\Activate.ps1
```

Jika PowerShell menolak aktivasi script, jalankan ini sekali sebelum aktivasi:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

5. Install dependency.

```powershell
pip install flask streamlit pandas joblib scikit-learn
```

### macOS

1. Buka Terminal.
2. Masuk ke folder project.

```bash
cd /path/ke/machine-learning/code
```

3. Buat virtual environment.

```bash
python3 -m venv .venv
```

4. Aktifkan virtual environment.

```bash
source .venv/bin/activate
```

5. Install dependency.

```bash
pip install flask streamlit pandas joblib scikit-learn
```

## Menjalankan Aplikasi Flask

Jalankan server Flask untuk membuka halaman web dan endpoint prediksi.

### Windows

```powershell
python app.py
```

### macOS

```bash
python3 app.py
```

Setelah itu buka browser ke:

```text
http://127.0.0.1:5000
```

## Menjalankan Aplikasi Streamlit

Kalau ingin tampilan interaktif via Streamlit, jalankan:

### Windows

```powershell
streamlit run streamlit_app.py
```

### macOS

```bash
streamlit run streamlit_app.py
```

Streamlit biasanya akan terbuka otomatis di browser. Jika tidak, buka alamat yang muncul di terminal.

## Cara Pakai

1. Pilih menu model yang ingin dicoba.
2. Isi parameter yang diminta.
3. Klik tombol prediksi atau klasifikasi.
4. Lihat hasil keluaran di layar.

## Catatan Model

- Folder `models/` dipakai untuk menyimpan file model dan encoder hasil training.
- Jika file model belum ada, aplikasi akan menampilkan hasil simulasi agar demo tetap bisa dicoba.
- Pada Streamlit, file model regresi yang dicari adalah `model_regresi.pkl` di root project. Jika file itu belum ada, aplikasi juga akan memakai simulasi.

## Jika Ingin Menambahkan Model Baru

Simpan file model yang sudah dilatih ke folder `models/`, lalu sesuaikan nama file pada `app.py` atau `streamlit_app.py` bila perlu.

## Troubleshooting

- Jika muncul error modul tidak ditemukan, pastikan virtual environment sudah aktif dan dependency sudah di-install.
- Jika PowerShell menolak aktivasi venv, gunakan langkah `Set-ExecutionPolicy` di atas.
- Jika hasil prediksi memakai simulasi, itu berarti file model belum ditemukan di lokasi yang diharapkan.
