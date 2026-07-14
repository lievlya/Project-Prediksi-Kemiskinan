import os
import time
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# ==========================================
# 1. LOAD ML MODELS (feature_label_encoders, scaler, model)
# ==========================================
MODEL_PATH = "models/v2/model_random_forest_kemiskinan.pkl"
SCALER_PATH = "models/v2/scaler.pkl"
ENCODER_PATH = "models/v2/feature_label_encoders.pkl"

model = None
scaler = None
encoders = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    with open(ENCODER_PATH, 'rb') as f:
        encoders = pickle.load(f)
    print("✅ Model ML berhasil dimuat!")
except Exception as e:
    print(f"❌ Gagal memuat Model ML: {e}")

# ==========================================
# 2. DATABASE CONNECTION WITH RETRY LOGIC
# ==========================================
def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "kemiskinan_db"),
                user=os.getenv("DB_USER", "admin"),
                password=os.getenv("DB_PASSWORD", "admin123password")
            )
            return conn
        except psycopg2.OperationalError:
            print("Database belum siap. Mencoba lagi dalam 3 detik...")
            time.sleep(3)
            retries -= 1
    return None

# ==========================================
# 3. ENDPOINTS API
# ==========================================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running", 
        "message": "API Prediksi Kemiskinan Berjalan Lancar!"
    })

@app.route("/predict", methods=["POST"])
def predict():
    if not model or not scaler:
        return jsonify({"error": "Model ML tidak ter-load di server!"}), 500
    
    try:
        # Ambil data input JSON dari Streamlit
        data = request.get_json()
        df = pd.DataFrame([data])
        
        # --- PREPROCESSING (Encoding & Scaling) ---
        # 1. Encode data kategorikal jika ada
        if encoders:
            for col, encoder in encoders.items():
                if col in df.columns:
                    try:
                        df[col] = encoder.transform(df[col])
                    except:
                        df[col] = 0 # Fallback value jika kategori baru tidak dikenal
        
        # 2. Scaling data numerik
        scaled_features = scaler.transform(df)
        
        # 3. Predict menggunakan Random Forest
        prediction = model.predict(scaled_features)
        result = int(prediction[0])
        
        # --- SIMPAN DATA PREDIKSI KE POSTGRESQL (Tugas DB) ---
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id SERIAL PRIMARY KEY,
                        input_data TEXT,
                        prediction_result INT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute(
                    "INSERT INTO predictions (input_data, prediction_result) VALUES (%s, %s)",
                    (str(data), result)
                )
                conn.commit()
                cursor.close()
                conn.close()
                print("✅ Hasil prediksi berhasil disimpan ke Database!")
            except Exception as db_err:
                print(f"❌ Gagal menyimpan ke database: {db_err}")

        # Response hasil akhir ke Streamlit
        return jsonify({
            "prediction": result,
            "status": "Miskin" if result == 1 else "Tidak Miskin"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
