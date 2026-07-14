#!/bin/bash

echo "=== MEMULAI PROSES ROLLING UPDATE BACKEND ==="

# 1. Tarik image backend terbaru dari GHCR
docker pull ghcr.io/bilabiw/project-prediksi-kemiskinan-be:v1.0.0

# 2. Matikan container lama jika masih hidup
docker stop poverty-backend-container || true
docker rm poverty-backend-container || true

# 3. Nyalakan container baru di port 8080 (menjalankan backend_app.py di dalam Docker)
docker run -d \
  --name poverty-backend-container \
  -p 8080:5000 \
  -e DB_HOST=localhost \
  ghcr.io/bilabiw/project-prediksi-kemiskinan-be:v1.0.0

echo "=== ROLLING UPDATE BERHASIL! ==="
