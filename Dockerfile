
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV MODEL_DIR=/app/models

EXPOSE 5000
CMD ["python", "api/server.py"]
