# Basis-Image mit Python 3
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten definieren
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Script in Container kopieren
COPY todoist2clockify.py ./

# Standard-Entrypoint
ENTRYPOINT ["python", "todoist2clockify.py"]
