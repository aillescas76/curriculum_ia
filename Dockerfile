FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=on \
    APP_HOME=/app

WORKDIR ${APP_HOME}

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        curl \
        git \
        libgomp1 \
        libopenblas-dev \
        libpq-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . ${APP_HOME}

RUN python -m pip install --upgrade pip \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi \
    && if [ -f pyproject.toml ]; then pip install --no-cache-dir .; fi

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser ${APP_HOME}

RUN cat <<'ENTRYPOINT' > /entrypoint.sh
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -gt 0 ]]; then
  exec "$@"
fi

service="${APP_SERVICE:-backend}"

case "$service" in
  backend)
    python manage.py migrate --noinput
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3}
    ;;
  streamlit)
    exec streamlit run frontend/app.py --server.address 0.0.0.0 --server.port ${STREAMLIT_SERVER_PORT:-8501}
    ;;
  worker)
    exec celery -A backend worker --loglevel=INFO
    ;;
  scheduler)
    exec celery -A backend beat --loglevel=INFO
    ;;
  *)
    echo "Unknown APP_SERVICE: $service" >&2
    exit 1
    ;;
esac
ENTRYPOINT

RUN chmod +x /entrypoint.sh

USER appuser

ENV PORT=8000 \
    STREAMLIT_SERVER_PORT=8501 \
    APP_SERVICE=backend \
    DJANGO_SETTINGS_MODULE=backend.settings \
    PYTHONPATH=${APP_HOME}

EXPOSE 8000 8501

ENTRYPOINT ["/entrypoint.sh"]
CMD []
