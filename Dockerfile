FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential gfortran libatlas-base-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["sh", "-c", "rasa run --enable-api --cors '*' --port ${PORT} --host 0.0.0.0 --debug"]
