# AGENTS.md

## Project overview
- "Curriculum Interactivo con IA" combina Django (API RAG) y Streamlit (UI) para exponer un currículum interactivo con chatbot.
- RAG offline: ingestión de CV sanitizado, chunking y FAISS; online: embeddings Gemini + recuperación + respuesta en streaming.
- Documentación clave: `docs/requisitos.md` (requisitos), `docs/plan_implementacion.md` (plan), `README.md` (resumen) y este archivo.

## Repo layout
- `backend/` proyecto Django con configuración base (`backend/settings.py`, `urls.py`, `asgi.py`, `wsgi.py`).
- `frontend/` aplicación Streamlit (`app.py`) con chat básico y `__init__.py`.
- `docs/` requisitos y plan de implementación.
- `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `pyproject.toml` y `.gitignore` en raíz.

## Setup commands
- Crear entorno virtual: `python3 -m venv .venv && source .venv/bin/activate` (Linux/macOS) o `.\.venv\Scripts\activate` (Windows).
- Instalar dependencias principales: `pip install -r requirements.txt`.
- Instalar en modo editable + extras dev: `pip install -e .[dev]`.
- Copiar variables: `cp .env.example .env` (crear `.env.example` si no existe) y completar claves (`GEMINI_API_KEY`, DB, Redis).

## Build & run
- Backend local: `DJANGO_DEBUG=true python backend/manage.py runserver 0.0.0.0:8000`.
- Streamlit local: `streamlit run frontend/app.py --server.port 8501`.
- Docker: `docker compose up --build` levanta backend, frontend, worker y Redis; monta volumen `vectorstore-data`.
- Comando de ingestión (a implementar): `python backend/manage.py build_vector_store --source docs/cv_sanitizado.pdf`.

## Tests
- Ejecutar suite principal: `pytest` (usa `backend.settings` por defecto).
- Tests Django focalizados: `pytest backend/tests`.
- Añadir/actualizar pruebas al tocar lógica RAG, endpoints y Streamlit helpers.
- Si hay regresiones, correr linters (`ruff`, `black`) antes de reintentar.

## Linting & formatting
- Revisar estilo: `ruff check .` (corrige con `ruff check . --fix`).
- Formatear Python: `black .` (line length 88).
- Mantener importaciones ordenadas; evitar introducir paquetes no usados en `requirements.txt` / `pyproject.toml`.

## Data & secrets
- CV sanitizado sin datos sensibles (requisito RNF-004); almacenar en `docs/` o `data/`.
- Vector store FAISS persistido en `vectorstore-data` (ignorado por git).
- Gestionar claves API vía `.env` y variables de entorno Docker/CI; nunca exponer en commits.

## Agent collaboration tips
- Usar `rg` para búsquedas y respetar las instrucciones del CLI: comandos con `['bash','-lc', ...]` y `workdir` explícito.
- No revertir cambios ajenos; si aparecen modificaciones inesperadas, consultar al usuario.
- Favorecer comentarios de código solo para bloques complejos; mantener ASCII.
- Si faltan endpoints o scripts referenciados (p.ej. `/chat/`), crear scaffolds mínimos antes de integrar lógica completa.

## Deployment notes
- Imagen base `Dockerfile` soporta modos `APP_SERVICE=backend|streamlit|worker|scheduler` (entrypoint corre migraciones y lanza servicio).
- Ajustar `docker-compose.yml` para producción (secretos, volúmenes persistentes) y añadir reverse proxy si es necesario.
- Smoke tests tras despliegue: `curl http://<host>:8000/health/` y abrir interfaz Streamlit en `:8501`.
