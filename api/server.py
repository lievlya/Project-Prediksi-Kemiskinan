import os
import random
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import library CORS
import joblib
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- 1. KONFIGURASI CORS ---
# Mengizinkan frontend Streamlit (localhost:8501) untuk mengakses API ini
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8501"}})

# Load model kemiskinan (joblib) jika ada
# model = joblib.load("model_kemiskinan.pkl")

@app.route('/api/predict', methods=['POST'])
def predict_poverty():
    # --- 2. SIMULASI ERROR (TUGAS INDIVIDU) ---
    # Simulasi 30% peluang error untuk menguji ketahanan frontend
    if random.random() < 0.3:
        return jsonify({
            "status": "error", 
            "message": "Terjadi kesalahan internal server saat memproses data kemiskinan."
        }), 500

    # --- 3. LOGIKA UTAMA API ---
    try:
        data = request.get_json()
        
        # Contoh pemrosesan data (sesuaikan dengan fitur modelmu)
        # pendapatan = data.get('pendapatan')
        # ... proses prediksi dengan model ...
        
        return jsonify({
            "status": "success",
            "prediction": "Miskin", # Nilai dummy hasil prediksi
            "poverty_probability": 0.76
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Berjalan di port 5000 untuk backend
    app.run(host='0.0.0.0', port=5000, debug=True)
