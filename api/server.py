import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- LOAD PKL ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

try:
    model = joblib.load(os.path.join(MODELS_DIR, "model_random_forest_kemiskinan.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    label_encoders = joblib.load(os.path.join(MODELS_DIR, "feature_label_encoders.pkl"))
    print("✅ SUCCESS: Model, Scaler, dan Encoders berhasil dimuat!")
except Exception as e:
    print(f"❌ Gagal memuat file pkl: {e}")
    model, scaler, label_encoders = None, None, None

def safe_extract(data, short_name, long_name, default_val=0.0):
    """Mengambil data dari JSON tanpa peduli huruf besar, kecil, atau nama panjang"""
    for key in [short_name, short_name.lower(), short_name.upper(), long_name]:
        if key in data and data[key] is not None:
            return float(data[key])
    return default_val

def safe_label_encode(le, value, default_val="JAWA TIMUR"):
    if le is None: return 0
    cleaned = str(value).strip().upper()
    for cls in le.classes_:
        if str(cls).strip().upper() == cleaned:
            return le.transform([cls])[0]
    return le.transform([default_val])[0] if default_val in le.classes_ else le.transform([le.classes_[0]])[0]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online"})

@app.route("/predict", methods=["POST"])
def predict():
    if not model or not scaler or not label_encoders:
        return jsonify({"status": "error", "message": "File PKL tidak lengkap di server."}), 500

    try:
        # Menerima JSON dari Streamlit
        data = request.get_json(force=True)
        
        # --- PARSING EXTRA AMAN (Case-Insensitive) ---
        provinsi = str(data.get("provinsi", data.get("Provinsi", "JAWA TIMUR")))
        kab_kota = str(data.get("kab_kota", data.get("Kab/Kota", "SURABAYA")))
        
        p0 = safe_extract(data, "p0", "Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota (Persen)", 9.5)
        rata_lama_sekolah = safe_extract(data, "rata_lama_sekolah", "Rata-rata Lama Sekolah Penduduk 15+ (Tahun)", 8.0)
        pengeluaran_per_kapita = safe_extract(data, "pengeluaran_per_kapita", "Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun)", 11000.0)
        ipm = safe_extract(data, "ipm", "Indeks Pembangunan Manusia", 71.0)
        umur_harapan_hidup = safe_extract(data, "umur_harapan_hidup", "Umur Harapan Hidup (Tahun)", 70.0)
        sanitasi_layak = safe_extract(data, "sanitasi_layak", "Persentase rumah tangga yang memiliki akses terhadap sanitasi layak", 80.0)
        air_minum_layak = safe_extract(data, "air_minum_layak", "Persentase rumah tangga yang memiliki akses terhadap air minum layak", 90.0)
        tingkat_pengangguran = safe_extract(data, "tingkat_pengangguran", "Tingkat Pengangguran Terbuka", 5.0)
        tingkat_partisipasi_kerja = safe_extract(data, "tingkat_partisipasi_kerja", "Tingkat Partisipasi Angkatan Kerja", 65.0)
        pdrb = safe_extract(data, "pdrb", "PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)", 20000000.0)

        # Encode Fitur Kategorikal
        prov_encoded = safe_label_encode(label_encoders.get("Provinsi"), provinsi, "JAWA TIMUR")
        kab_encoded = safe_label_encode(label_encoders.get("Kab/Kota"), kab_kota, "SURABAYA")

        # Susun 12 Kolom Sesuai Cetakan Scaler
        feature_names = [
            "Provinsi", "Kab/Kota", 
            "Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota (Persen)",
            "Rata-rata Lama Sekolah Penduduk 15+ (Tahun)",
            "Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun)",
            "Indeks Pembangunan Manusia", "Umur Harapan Hidup (Tahun)",
            "Persentase rumah tangga yang memiliki akses terhadap sanitasi layak",
            "Persentase rumah tangga yang memiliki akses terhadap air minum layak",
            "Tingkat Pengangguran Terbuka", "Tingkat Partisipasi Angkatan Kerja",
            "PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)"
        ]

        input_data = [[
            prov_encoded, kab_encoded, p0, rata_lama_sekolah, 
            pengeluaran_per_kapita, ipm, umur_harapan_hidup, 
            sanitasi_layak, air_minum_layak, tingkat_pengangguran, 
            tingkat_partisipasi_kerja, pdrb
        ]]

        df_input = pd.DataFrame(input_data, columns=feature_names)
        
        # PRINT DI TERMINAL FLASK UNTUK INSPEKSI MANUAl
        print("\n=== DATA YANG DIBACA FLASK PROSES ===")
        print(df_input.to_dict(orient='records')[0])
        print("=====================================\n")

        # Proses Skala & Prediksi
        X_scaled = scaler.transform(df_input)
        df_scaled = pd.DataFrame(X_scaled, columns=feature_names)
        raw_prediction = model.predict(df_scaled)[0]

        # Mapping Output
        mapping = {0: "Rendah", 1: "Sedang", 2: "Tinggi"}
        prediction_label = mapping.get(int(raw_prediction), str(raw_prediction))

        # Mengembalikan hasil prediksi + data debug
        return jsonify({
            "status": "success",
            "prediction": prediction_label,
            "data_terbaca_di_server": {
                "p0_terbaca": p0,
                "ipm_terbaca": ipm,
                "pdrb_terbaca": pdrb
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)