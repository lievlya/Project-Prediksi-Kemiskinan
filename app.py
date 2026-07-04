import streamlit as st
import pandas as pd
import numpy as np
import requests  # Digunakan sebagai pengganti fetch/axios di Python
import os
import streamlit as st

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="Prediksi Kemiskinan", layout="wide")

# --- KONFIGURASI API BACKEND ---
# Sesuaikan URL ini dengan alamat API yang disediakan oleh tim Backend kamu (misal: FastAPI / Flask)
API_URL = "http://127.0.0.1:8000/predict" 

# --- INITIALIZATION SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Landing"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- FUNGSI NAVIGASI ---
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 1. BLUEPRINT A: LANDING PAGE
# ==========================================
if st.session_state.page == "Landing":
    st.title("📌 Prediksi Kemiskinan")
    st.write("Analisis data metrik dengan model Machine Learning untuk prediksi tingkat kemiskinan daerah.")
    
    if st.button("Mulai Analisis / Masuk ke Sistem"):
        if st.session_state.logged_in:
            go_to("Dashboard")
        else:
            go_to("Login")
            
    st.write("---")
    st.caption("© 2026 Proyek Analisis Kemiskinan")

# ==========================================
# 2. BLUEPRINT B: HALAMAN LOGIN
# ==========================================
elif st.session_state.page == "Login":
    st.markdown("<h2 style='text-align: center;'>Form Container</h2>", unsafe_allow_html=True)
    
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
# 3. BLUEPRINT C: HALAMAN DASHBOARD (Uji Analisis & Grafik)
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
    c1.metric(label="Total Data", value="2,650", delta="Regional Indikator")
    c2.metric(label="Tingkat Kemiskinan Saat Ini", value="43.5%", delta="Tingkat Maksimal")
    c3.metric(label="Tingkat Kemiskinan Sasaran", value="10.1%", delta="-3.3%")

    st.write("---")
    
    st.subheader("🔮 Form Input Prediksi")
    pendapatan = st.number_input("Rata-rata Pendapatan (Rupiah)", min_value=0, value=1500000)
    pengeluaran = st.number_input("Rata-rata Pengeluaran (Rupiah)", min_value=0, value=1200000)
    
    if st.button("Cek Analisa Kemiskinan"):
        # Data payload JSON yang dikirim ke API Backend
        payload = {
            "pendapatan": pendapatan,
            "pengeluaran": pengeluaran
        }
        
        # 1. MENANGANI KONDISI LOADING (UI Spinner)
        with st.spinner("Mengirim data ke server dan memproses prediksi... Mohon tunggu."):
            try:
                # Memanggil API Backend (Setara dengan fetch/axios POST request)
                response = requests.post(API_URL, json=payload, timeout=10)
                
                # JIKA BERHASIL (Status Code 200)
                if response.status_code == 200:
                    result = response.json()
                    # Ambil key hasil prediksi dari respons JSON backend (misal backend mengembalikan {"prediction": "Miskin"})
                    hasil_prediksi = result.get("prediction", "Data Berhasil Diproses")
                    
                    # 2. MENANGANI KONDISI SUCCESS PADA UI
                    st.success(f"🎉 Analisis Berhasil! Hasil Prediksi: {hasil_prediksi}")
                    
                    # Tampilkan Grafik Hasil Analisis
                    st.subheader("📈 Structured Charts Hasil Analisis")
                    chart_data = pd.DataFrame(
                        np.random.randn(20, 3),
                        columns=['Metrik A', 'Metrik B', 'Metrik C']
                    )
                    st.bar_chart(chart_data)
                
                # JIKA SERVER RESPONS NYA ERROR (Misal 404, 500, dll)
                else:
                    # 3. MENANGANI KONDISI ERROR DARI RESPONS SERVER
                    st.error(f"❌ Server Error ({response.status_code}): Gagal mendapatkan hasil analisis dari backend.")
                    st.info("Saran: Periksa kembali kecocokan API Contract data input dengan Backend.")
                    
            except requests.exceptions.ConnectionError:
                # 3. MENANGANI KONDISI ERROR JIKA BACKEND BELUM NYALA / TIME OUT
                st.error("❌ Connection Error: Tidak dapat terhubung ke server API Backend.")
                st.warning("Pastikan server Backend sudah dijalankan oleh tim Backend kamu di lokal.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan sistem: {str(e)}")