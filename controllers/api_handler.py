"""
controllers/api_handler.py
---------------------------
Backend "API handler" untuk aplikasi Prediksi Kemiskinan (Streamlit).

Analog dengan konsep RESTful controller di Minggu 9: fungsi-fungsi di sini
berperan seperti endpoint (GET /predict) yang dipanggil oleh layer View
(Streamlit UI). Backend Developer bertanggung jawab memastikan fungsi ini
mengembalikan struktur data yang konsisten agar Frontend/View tidak error
saat rendering (lihat Minggu 10 - Sinkronisasi Frontend-Backend).
"""

import os
import joblib
import pandas as pd
from dotenv import load_dotenv

# Load variabel dari .env (path model, dsb) - lihat Minggu 9: Keamanan Kode & File Sensitif
load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "models/model_random_forest_kemiskinan.pkl")
ENCODER_PATH = os.getenv("ENCODER_PATH", "models/feature_label_encoders.pkl")
SCALER_PATH = os.getenv("SCALER_PATH", "models/scaler.pkl")

# Urutan fitur HARUS sama persis dengan urutan saat scaler/model di-training.
# Ini adalah "API Contract" versi model ML - jika frontend mengirim data
# dengan urutan/nama field berbeda, prediksi akan salah atau error.
FEATURE_ORDER = [
    "Provinsi",
    "Kab/Kota",
    "Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota (Persen)",
    "Rata-rata Lama Sekolah Penduduk 15+ (Tahun)",
    "Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun)",
    "Indeks Pembangunan Manusia",
    "Umur Harapan Hidup (Tahun)",
    "Persentase rumah tangga yang memiliki akses terhadap sanitasi layak",
    "Persentase rumah tangga yang memiliki akses terhadap air minum layak",
    "Tingkat Pengangguran Terbuka",
    "Tingkat Partisipasi Angkatan Kerja",
    "PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)",
]

# Kolom yang di-label-encode (kategori/berbentuk string bertanda koma)
_model = None
_encoders = None
_scaler = None
_is_loading = True  # simulasi "Loading State" seperti di Minggu 10


def load_artifacts():
    """Muat model, encoder, dan scaler sekali saja (cache in-memory)."""
    global _model, _encoders, _scaler, _is_loading
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        _encoders = joblib.load(ENCODER_PATH)
        _scaler = joblib.load(SCALER_PATH)
        _is_loading = False
    return _model, _encoders, _scaler


def get_provinsi_list():
    """Endpoint pembantu: kembalikan daftar Provinsi valid untuk dropdown UI."""
    _, encoders, _ = load_artifacts()
    return sorted(encoders["Provinsi"].classes_.tolist())


def get_kabkota_list():
    """Endpoint pembantu: kembalikan daftar Kab/Kota valid untuk dropdown UI."""
    _, encoders, _ = load_artifacts()
    return sorted(encoders["Kab/Kota"].classes_.tolist())


def _preprocess(input_dict: dict) -> pd.DataFrame:
    """Ubah input mentah dari form UI menjadi data siap-prediksi."""
    _, encoders, scaler = load_artifacts()

    df = pd.DataFrame([input_dict])
    missing = [c for c in FEATURE_ORDER if c not in df.columns]
    if missing:
        raise ValueError(f"Field wajib belum diisi: {missing}")

    df = df[FEATURE_ORDER]

    for col, le in encoders.items():
        value = str(df.at[0, col])
        if value not in le.classes_:
            raise ValueError(
                f"Nilai '{value}' pada field '{col}' tidak dikenali model. "
                f"Gunakan dropdown/nilai yang sudah tersedia di data training."
            )
        df[col] = le.transform([value])

    return scaler.transform(df)


def predict_kemiskinan(input_dict: dict) -> dict:
    """
    Fungsi utama (setara endpoint POST /predict).

    Parameters
    ----------
    input_dict : dict
        Data satu baris wilayah, key harus sesuai FEATURE_ORDER.

    Returns
    -------
    dict
        Struktur response konsisten: {"status", "data" / "message"}
        Frontend (Streamlit UI) hanya perlu membaca struktur ini,
        tidak perlu tahu detail model di baliknya.
    """
    try:
        model, _, _ = load_artifacts()
        X = _preprocess(input_dict)

        pred = int(model.predict(X)[0])
        proba = model.predict_proba(X)[0]

        return {
            "status": "success",
            "data": {
                "prediction": pred,
                "label": "Rawan Miskin" if pred == 1 else "Tidak Rawan Miskin",
                "probability": {
                    "tidak_miskin": round(float(proba[0]), 4),
                    "miskin": round(float(proba[1]), 4),
                },
            },
        }
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    except Exception as e:
        return {"status": "error", "message": f"Terjadi kesalahan internal: {e}"}


if __name__ == "__main__":
    # Simulasi pemanggilan endpoint, mirip contoh get_users() di Minggu 9
    contoh_input = {
        "Provinsi": "ACEH",
        "Kab/Kota": "Aceh Barat",
        "Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota (Persen)": "10",
        "Rata-rata Lama Sekolah Penduduk 15+ (Tahun)": "10",
        "Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun)": 8000,
        "Indeks Pembangunan Manusia": "48,68",
        "Umur Harapan Hidup (Tahun)": "58",
        "Persentase rumah tangga yang memiliki akses terhadap sanitasi layak": "11,43",
        "Persentase rumah tangga yang memiliki akses terhadap air minum layak": "19,78",
        "Tingkat Pengangguran Terbuka": "0,79",
        "Tingkat Partisipasi Angkatan Kerja": " 57,90 ",
        "PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)": 5000000,
    }
    print(predict_kemiskinan(contoh_input))
