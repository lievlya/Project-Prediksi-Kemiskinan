# Menggunakan base image Python resmi yang ringan
FROM python:3.10-slim

# Menentukan direktori kerja di dalam kontainer
WORKDIR /app

# Menyalin file requirements ke dalam kontainer
COPY requirements.txt .

# Menginstal library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode proyek ke direktori kerja kontainer
COPY . .

# MENENTUKAN VARIABEL ALAMAT API (Instruksi Minggu 12)
ENV API_URL=http://127.0.0.1:8000/predict

# Membuka port default Streamlit (8501)
EXPOSE 8501

# Perintah untuk menjalankan Streamlit saat kontainer dinyalakan
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]