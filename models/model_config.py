
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "models/model_random_forest_kemiskinan.pkl")
ENCODER_PATH = os.getenv("ENCODER_PATH", "models/feature_label_encoders.pkl")
SCALER_PATH = os.getenv("SCALER_PATH", "models/scaler.pkl")

# Contoh field sensitif tambahan jika nanti model di-host di cloud storage
# (S3/GDrive/HuggingFace) - TIDAK pernah di-commit ke Git, hanya ada di .env
MODEL_STORAGE_API_KEY = os.getenv("MODEL_STORAGE_API_KEY", "")


def verify_config():
    """Pastikan semua file konfigurasi wajib tersedia sebelum app dijalankan."""
    missing = [
        p for p in [MODEL_PATH, ENCODER_PATH, SCALER_PATH]
        if not os.path.exists(p)
    ]
    if missing:
        raise FileNotFoundError(
            f"File model tidak ditemukan: {missing}. "
            f"Cek kembali isi .env dan pastikan file .pkl ada di folder models/."
        )
    return True


if __name__ == "__main__":
    print("MODEL_PATH  :", MODEL_PATH)
    print("ENCODER_PATH:", ENCODER_PATH)
    print("SCALER_PATH :", SCALER_PATH)
    print("Config valid:", verify_config())
