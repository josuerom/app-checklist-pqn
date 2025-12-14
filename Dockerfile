FROM python:3.11-slim

# Metadata
LABEL maintainer="josue.romero@spradling.group"
LABEL description="Lista de Chequeo Alistamiento de Equipos"
LABEL version="1.1.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Pasar todo el proyecto a contenedor
COPY . .

# Exponer puerto
EXPOSE 9015

# Usuario no root (seguridad)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:9015/')"

# Comando de inicio
CMD ["gunicorn", "-b", "0.0.0.0:9015", "-w", "2", "--timeout", "120", "app:app"]