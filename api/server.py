import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Mengizinkan koneksi cross-origin dari frontend Streamlit

# --- SETUP PATH FILE PKL ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

model_path = os.path.join(MODELS_DIR, "model_random_forest_kemiskinan.pkl")
scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
encoders_path = os.path.join(MODELS_DIR, "feature_label_encoders.pkl")

# Load model, scaler, dan encoders
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    with open(encoders_path, "rb") as f:
        label_encoders = pickle.load(f)
    print("✅ Model, Scaler, dan Label Encoders berhasil dimuat!")
except Exception as e:
    print(f"❌ Gagal memuat file pkl: {e}")
    model, scaler, label_encoders = None, None, None

# Mapping hasil prediksi numerik (0, 1, 2) kembali ke teks deskriptif
CLASS_MAPPING = {
    0: "Rendah",
    1: "Sedang",
    2: "Tinggi"
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "API Prediksi Kemiskinan siap menerima data!"
    })

@app.route("/predict", methods=["POST"])
def predict():
    if not model or not scaler or not label_encoders:
        return jsonify({
            "status": "error",
            "message": "Infrastruktur model ML belum terpasang dengan benar di server."
        }), 500

    try:
        data = request.get_json(force=True)

        # Ambil input dari JSON dengan nilai default (median nasional dari notebook kamu)
        provinsi = data.get("provinsi", "JAWA TIMUR")
        kab_kota = data.get("kab_kota", "SURABAYA")
        p0 = float(data.get("p0", 9.0))
        rata_lama_sekolah = float(data.get("rata_lama_sekolah", 8.0))
        pengeluaran_per_kapita = float(data.get("pengeluaran_per_kapita", 11000.0))
        ipm = float(data.get("ipm", 71.0))
        umur_harapan_hidup = float(data.get("umur_harapan_hidup", 71.5))
        sanitasi_layak = float(data.get("sanitasi_layak", 80.0))
        air_minum_layak = float(data.get("air_minum_layak", 90.0))
        tingkat_pengangguran = float(data.get("tingkat_pengangguran", 5.0))
        tingkat_partisipasi_kerja = float(data.get("tingkat_partisipasi_kerja", 68.0))
        pdrb = float(data.get("pdrb", 20000000.0))

        # --- STEP 1: ENCODING CATEGORICAL FEATURES ---
        # Encode 'Provinsi'
        le_prov = label_encoders.get("Provinsi")
        try:
            prov_encoded = le_prov.transform([provinsi.upper()])[0]
        except:
            prov_encoded = le_prov.transform([le_prov.classes_[0]])[0] # Fallback jika data tidak dikenali

        # Encode 'Kab/Kota'
        le_kab = label_encoders.get("Kab/Kota")
        try:
            kab_encoded = le_kab.transform([kab_kota.upper()])[0]
        except:
            kab_encoded = le_kab.transform([le_kab.classes_[0]])[0] # Fallback jika data tidak dikenali

        # --- STEP 2: STRUKTURKAN FITUR SESUAI DENGAN SCALER (12 KOLOM) ---
        raw_features = np.array([[
            prov_encoded,
            kab_encoded,
            p0,
            rata_lama_sekolah,
            pengeluaran_per_kapita,
            ipm,
            umur_harapan_hidup,
            sanitasi_layak,
            air_minum_layak,
            tingkat_pengangguran,
            tingkat_partisipasi_kerja,
            pdrb
        ]])

        # --- STEP 3: NORMALSASI DATA MENGGUNAKAN SCALER.PKL ---
        feature_names = [
            "Provinsi", "Kab/Kota", 
            "Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota (Persen)",
            "Rata-rata Lama Sekolah Penduduk 15+ (Tahun)",
            "Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun)",
            "Indeks Pembangunan Manusia",
            "Umur Harapan Hidup (Tahun)",
            "Persentase rumah tangga yang memiliki akses terhadap sanitasi layak",
            "Persentase rumah tangga yang memiliki akses terhadap air minum layak",
            "Tingkat Pengangguran Terbuka",
            "Tingkat Partisipasi Angkatan Kerja",
            "PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)"
        ]
        features_df = pd.DataFrame(raw_features, columns=feature_names)
        scaled_features = scaler.transform(features_df)

        # --- STEP 4: PREDIKSI MENGGUNAKAN RANDOM FOREST ---
        prediction_idx = int(model.predict(scaled_features)[0])
        prediction_label = CLASS_MAPPING.get(prediction_idx, "Tidak Diketahui")

        return jsonify({
            "status": "success",
            "prediction_class": prediction_idx,
            "prediction": prediction_label
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan di server: {str(e)}"
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
