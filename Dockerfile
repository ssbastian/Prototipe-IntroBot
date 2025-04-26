FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Puerto expuesto (debe coincidir con el de Render)
EXPOSE 10000

# Comando clave: --host 0.0.0.0 es obligatorio para Render
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000"]
