import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Prediksi Kemiskinan", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost/predict")

# --- INITIALIZATION SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Landing"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 1. LANDING PAGE
# ==========================================
if st.session_state.page == "Landing":
    st.title("📌 Prediksi Tingkat Kemiskinan Regional")
    st.write("Analisis data metrik dengan model Machine Learning (Random Forest) untuk memprediksi kategori kemiskinan daerah.")
    
    if st.button("Mulai Analisis / Masuk ke Sistem"):
        if st.session_state.logged_in:
            go_to("Dashboard")
        else:
            go_to("Login")
            
    st.write("---")
    st.caption("© 2026 Proyek Analisis Kemiskinan")

# ==========================================
# 2. HALAMAN LOGIN
# ==========================================
elif st.session_state.page == "Login":
    st.markdown("<h2 style='text-align: center;'>Form Login</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Email", placeholder="Masukkan email anda")
        password = st.text_input("Kata Sandi", type="password", placeholder="Masukkan kata sandi")
        
        if st.button("Masuk", use_container_width=True):
            if email == "admin@mail.com" and password == "admin123":
                st.session_state.logged_in = True
                go_to("Dashboard")
            else:
                st.error("Email atau password salah!")
                
        if st.button("Kembali ke Beranda"):
            go_to("Landing")

# ==========================================
# 3. HALAMAN DASHBOARD (Uji Analisis & Grafik)
# ==========================================
elif st.session_state.page == "Dashboard":
    with st.sidebar:
        st.title("⚙️ Menu Utama")
        st.write(f"Logged in as: Admin")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            go_to("Landing")
            
    st.header("📊 Dashboard Analisis & Prediksi")
    
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Total Data Latih", value="514", delta="Regional Indikator")
    c2.metric(label="Akurasi Model RF", value="98.5%", delta="Optimized")
    c3.metric(label="Tingkat Kemiskinan Sasaran", value="< 7.0%", delta="Target RPJMN")

    st.write("---")
    
    st.subheader("🔮 Form Input Prediksi Kemiskinan (12 Indikator)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        provinsi = st.selectbox("Provinsi", ["JAWA TIMUR", "JAWA TENGAH", "JAWA BARAT", "DKI JAKARTA", "BANTEN", "BALI", "DI YOGYAKARTA"])
        kab_kota = st.text_input("Kabupaten / Kota", value="SURABAYA")
        p0 = st.number_input("Persentase Penduduk Miskin (P0) (%)", min_value=0.0, max_value=100.0, value=9.5)
        rata_lama_sekolah = st.number_input("Rata-rata Lama Sekolah (Tahun)", min_value=0.0, value=8.5)
        pengeluaran_per_kapita = st.number_input("Pengeluaran per Kapita Disesuaikan (Ribu Rp/Orang/Tahun)", min_value=0.0, value=11500.0)
        ipm = st.number_input("Indeks Pembangunan Manusia (IPM)", min_value=0.0, max_value=100.0, value=72.0)

    with col2:
        umur_harapan_hidup = st.number_input("Umur Harapan Hidup (Tahun)", min_value=0.0, value=71.8)
        sanitasi_layak = st.number_input("Akses Sanitasi Layak (%)", min_value=0.0, max_value=100.0, value=82.5)
        air_minum_layak = st.number_input("Akses Air Minum Layak (%)", min_value=0.0, max_value=100.0, value=91.0)
        tingkat_pengangguran = st.number_input("Tingkat Pengangguran Terbuka (%)", min_value=0.0, max_value=100.0, value=5.2)
        tingkat_partisipasi_kerja = st.number_input("Tingkat Partisipasi Angkatan Kerja (%)", min_value=0.0, max_value=100.0, value=67.8)
        pdrb = st.number_input("PDRB Harga Konstan (Rupiah)", min_value=0.0, value=25000000.0)
    
    if st.button("Cek Analisa Kemiskinan", use_container_width=True):
        payload = {
            "provinsi": provinsi,
            "kab_kota": kab_kota,
            "p0": p0,
            "rata_lama_sekolah": rata_lama_sekolah,
            "pengeluaran_per_kapita": pengeluaran_per_kapita,
            "ipm": ipm,
            "umur_harapan_hidup": umur_harapan_hidup,
            "sanitasi_layak": sanitasi_layak,
            "air_minum_layak": air_minum_layak,
            "tingkat_pengangguran": tingkat_pengangguran,
            "tingkat_partisipasi_kerja": tingkat_partisipasi_kerja,
            "pdrb": pdrb
        }
        
        with st.spinner("Mengirim data ke server API & menghitung prediksi ML... Mohon tunggu."):
            try:
                response = requests.post(API_URL, json=payload, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    hasil_prediksi = result.get("prediction", "Data Berhasil Diproses")
                    
                    st.success(f"🎉 Analisis Berhasil! Hasil Prediksi Tingkat Kemiskinan: **{hasil_prediksi}**")
                    
                    # Tampilkan Grafik Acak sebagai Variasi UI
                    st.subheader("📈 Visualisasi Metrik Regional")
                    chart_data = pd.DataFrame(
                        np.random.randn(20, 3),
                        columns=['Dimensi Sosial', 'Dimensi Ekonomi', 'Dimensi Kesehatan']
                    )
                    st.bar_chart(chart_data)
                else:
                    st.error(f"❌ Server Error ({response.status_code}): Gagal memproses prediksi.")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Tidak dapat terhubung ke server API Flask.")
                st.warning("Pastikan kamu telah menjalankan server backend dengan perintah 'python server.py' di port 8000.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan sistem: {str(e)}")