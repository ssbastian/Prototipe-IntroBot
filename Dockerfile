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
EXPOSE 5055

CMD ["rasa", "run", "actions", "--port", "5055", "--host", "0.0.0.0"]
