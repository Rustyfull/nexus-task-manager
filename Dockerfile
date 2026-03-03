# --- Stage 1: Builder ---
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Création du virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
# On installe dans le venv (pas de --user ici)
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Final ---
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# On récupère TOUT le venv du builder
COPY --from=builder /opt/venv /opt/venv

# On met le venv en priorité dans le PATH
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . .

# On crée l'utilisateur et on lui donne les droits sur l'app
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Plus besoin de "python -m", uvicorn est directement dans le PATH du venv
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]