# Verwende ein leichtgewichtiges Python-Image als Basis
FROM python:3.8-slim

# Setze das Arbeitsverzeichnis innerhalb des Containers
WORKDIR /app

# Kopiere die Anforderungen in den Container und installiere sie
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Codes in den Container
COPY . .

# Starte den FastAPI-Server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
