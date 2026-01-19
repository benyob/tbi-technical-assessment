FROM python:3.10-slim

# --- System-level guarantees ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- Install minimal OS deps ---
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- Create working directory ---
WORKDIR /home/src

# --- Install Python deps first (layer caching) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy application code ---
COPY . .

# --- Expose required port ---
EXPOSE 8080

# --- Entrypoint ---
CMD ["python", "-m", "app.main"]
