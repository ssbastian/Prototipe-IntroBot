FROM python:3.8-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar primero los archivos de requisitos para aprovechar la caché de Docker
COPY requirements.txt .

# Crear y activar el entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos
COPY . .

# Puerto expuesto (Render usará el que especifiques en sus configuraciones)
EXPOSE 10000

# Comando para ejecutar Rasa (usando shell form para variables de entorno)
CMD rasa run --enable-api --cors "*" --port $PORT
