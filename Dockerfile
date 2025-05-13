# 🧱 Base image with Python and pip
FROM python:3.12.3 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 🔧 Set up virtual environment
RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt

# 🏗️ Slim runtime image
FROM python:3.12.3-slim

WORKDIR /app

# 🧬 Copy venv from builder
COPY --from=builder /app/.venv .venv/

# 🧾 Copy app files
COPY . .

# 🚀 Run FastAPI using Uvicorn
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
