# Currículum Interactivo con IA

Aplicación web que transforma un currículum tradicional en una experiencia interactiva impulsada por IA. Reclutadores y equipos de contratación pueden explorar el perfil del candidato mediante una landing responsiva y un chatbot que responde en lenguaje natural usando Recuperación Aumentada por Generación (RAG).

## Características clave
- **Currículum completo en la landing** con descarga en PDF y diseño adaptable a móviles (FR-001, FR-002, FR-003).
- **Chatbot conversacional** integrado con mensaje de bienvenida, sugerencias de preguntas y memoria de contexto (FR-004 – FR-008).
- **Respuestas fundamentadas** exclusivamente en el currículum sanitizado utilizando FAISS + Gemini y manejo elegante de preguntas fuera de alcance (FR-007, FR-009).
- **Streaming de respuestas** para mejorar la experiencia del usuario (FR-010).

## Arquitectura prevista
```
Streamlit UI ──► Django API ──► FAISS Vector Store ──► Gemini API
    ▲              │                │                   │
    └─(Websocket/HTTP)◄─ Memoria Conversacional ◄───────┘
```
- **Pipeline offline**: ingestión del currículum, fragmentación, embeddings y almacenamiento en FAISS.
- **Pipeline online**: embedding de la consulta, búsqueda de similitud, construcción del prompt y respuesta en streaming.

## Pila tecnológica
- **Backend**: Python 3.9+, Django, Django REST Framework, LangChain.
- **Modelo IA**: Google Gemini (gemini-2.5-flash) para embeddings y chat.
- **Vector store**: FAISS.
- **Frontend**: Streamlit.
- **Opcionales**: Celery + Redis para llamadas asíncronas de alta latencia.
- **Infraestructura**: Docker / Docker Compose para orquestación y despliegue (Render, Heroku, Vercel, etc.).

## Preparación del entorno (referencia)
1. Clonar el repositorio y crear un entorno virtual (`python -m venv .venv`).
2. Activar el entorno e instalar dependencias (archivo `requirements.txt` o `pyproject.toml` una vez definidos).
3. Configurar variables de entorno: copiar `.env.example` (por crear) y establecer credenciales como `GEMINI_API_KEY`.
4. Ejecutar el comando de ingestión (`manage.py build_vector_store` o script equivalente) tras actualizar el currículum sanitizado.
5. Levantar servicios con `docker compose up` para entorno unificado de desarrollo.

## Variables de entorno sugeridas
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `GEMINI_API_KEY`
- `FAISS_INDEX_PATH`
- `REDIS_URL` (si Celery está habilitado)
- `STREAMLIT_SERVER_PORT`

## Estructura propuesta del repositorio
```
.
├── docs/
│   ├── requisitos.md
│   └── plan_implementacion.md
├── AGENTS.md
├── README.md
└── .gitignore
```
Se ampliará con directorios `backend/`, `frontend/`, `docker/`, etc., durante la implementación.

## Calidad y observabilidad
- Linting con Ruff/Flake8 y formateo con Black.
- Pruebas unitarias e integración (pytest) para el pipeline RAG y endpoints REST.
- Logging estructurado y métricas de latencia/error para seguimiento de la experiencia del chatbot.

## Despliegue
1. Construir imágenes Docker para backend y frontend.
2. Publicar en un registro y configurar la plataforma objetivo (Render/Heroku para Django, Streamlit Cloud o Vercel para la UI).
3. Gestionar secretos mediante variables de entorno o gestores (p. ej. Vault, Secret Manager).
4. Ejecutar smoke tests post despliegue (health check, flujo de chat, descarga de PDF).

## Documentación relacionada
- `docs/requisitos.md`: Especificación completa de requisitos (FR/RNF/US).
- `docs/plan_implementacion.md`: Plan paso a paso para construir la solución.
- `AGENTS.md`: Descripción de los agentes implicados en el pipeline RAG y consideraciones operativas.

## Próximos pasos
- Implementar la estructura básica de Django + Streamlit según el plan.
- Automatizar la ingestión del currículum sanitizado y la generación del vector store.
- Integrar la experiencia conversacional, pruebas y despliegue contenerizado.
