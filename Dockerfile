# Usa Python 3.8 (compatible con Rasa)
FROM python:3.8-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instala librerías del sistema necesarias
RUN apt-get update && \
    apt-get install -y build-essential gfortran libatlas-base-dev && \
    rm -rf /var/lib/apt/lists/*

# Copia tu proyecto al contenedor
COPY . /app

# Crea un entorno virtual (opcional pero recomendable)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto de Rasa (¡DEBE coincidir con el puerto en CMD!)
EXPOSE 5005  

# Comando para iniciar el bot
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
