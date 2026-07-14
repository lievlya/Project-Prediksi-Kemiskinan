# STAGE 1: Builder (Proses Instalasi Library)
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# STAGE 2: Production (Hasil Akhir yang Ringan)
FROM python:3.10-slim
WORKDIR /app

# Menyalin hasil instalasi library dari stage builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Tetap pertahankan konfigurasi asli proyekmu
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV MODEL_DIR=/app/models
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000
CMD ["python", "api/server.py"]
