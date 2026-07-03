import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8501"}})

# --- TUGAS INDIVIDU: BACA APP_ENV ---
# Membaca environment variable APP_ENV, default ke 'development' jika tidak diatur
app_env = os.getenv("APP_ENV", "development")
print(f"Aplikasi berjalan di lingkungan: {app_env}")
# ------------------------------------

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "success",
        "environment": app_env,
        "message": "Backend model kemiskinan aktif."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=(app_env == "development"))
