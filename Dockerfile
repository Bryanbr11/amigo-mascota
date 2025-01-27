FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_TIMEOUT=100
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_RETRIES=3

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN pip install --no-cache-dir --upgrade pip

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .