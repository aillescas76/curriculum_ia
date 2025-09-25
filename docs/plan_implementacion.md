# Plan de Implementacion del Curriculum Interactivo con IA

## 1. Descubrimiento y alineacion
1. Revisar en detalle `docs/requisitos.md` para confirmar alcance, publico objetivo y restricciones tecnicas.
2. Recopilar curriculum sanitizado en formato PDF o Markdown y validar que no contenga datos sensibles (RNF-004).
3. Definir entregables iniciales (MVP) y considerar hitos iterativos: informacion estatica del curriculum, chatbot RAG, despliegue contenerizado.

## 2. Preparacion del entorno
1. Crear repositorio base de Django + Streamlit; configurar gestion de versiones y CI minimo.
2. Definir variables de entorno requeridas (por ejemplo `GEMINI_API_KEY`, rutas de FAISS, configuracion de Redis) y documentarlas.
3. Configurar entorno virtual Python 3.9+, instalar dependencias primarias: Django, Django REST Framework, LangChain, google-generativeai, FAISS, Streamlit, Redis (cliente) y herramientas de lint/testing.
4. Preparar imagen base de Docker con servicios necesarios (app, worker opcional, Redis si se autohospeda).

## 3. Pipeline RAG offline
1. Implementar script/gestion Django para ingestión del curriculum:
   - cargar documento sanitizado,
   - fragmentar texto en chunks consistentes con la longitud del modelo,
   - generar embeddings via API de Gemini,
   - persistir vector store FAISS en disco (estructura versionada).
2. Crear pruebas unitarias que validen fragmentacion y recuperacion basica.
3. Automatizar ejecucion bajo comando (por ejemplo `manage.py build_vector_store`) y documentar pasos.

## 4. Backend Django + API
1. Crear proyecto Django y app dedicada al chatbot.
2. Configurar modelos o capas de acceso para vector store FAISS (lectura) y almacenamiento de historial si se persiste.
3. Exponer endpoints REST:
   - `GET /health` para monitoreo basico,
   - `POST /chat` que reciba pregunta, contexto conversacional y devuelva respuesta en streaming o chunked.
4. Implementar servicio que ejecute flujo RAG online (embedding de consulta, busqueda FAISS, construccion de prompt, llamada a Gemini, manejo de OOS segun FR-009).
5. Integrar LangChain para orquestar memoria conversacional y streaming (FR-008, FR-010).
6. Añadir tests unitarios/integracion que cubran OOS, seguimiento de contexto y latencia simulada.

## 5. Interfaz de usuario (Streamlit)
1. Diseñar landing responsiva que muestre curriculum completo y boton visible `Descargar PDF` (FR-001, FR-002, FR-003).
2. Implementar componente de chat con:
   - mensaje de bienvenida con sugerencias (FR-005),
   - input y log conversacional,
   - streaming de respuestas recibido desde backend.
3. Integrar llamadas al endpoint `/chat`, gestionar tokens de latencia (<2 s RNF-007) mostrando indicador de escritura.
4. Validar comportamiento en escritorio, tablet, mobile (US-005) y ajustar estilos.

## 6. Integracion extremo a extremo
1. Conectar Streamlit con API de Django en entorno local (Docker compose o similar) asegurando CORS y autenticacion si aplica.
2. Ensayar flujo completo: pregunta, recuperacion FAISS, respuesta, manejo de preguntas fuera de alcance.
3. Medir tiempo de carga inicial y optimizar (cache de assets, configuracion de servidor) para cumplir RNF-006.

## 7. Calidad y observabilidad
1. Configurar linting (ruff/flake8), formateo (black) y pruebas automatizadas en CI.
2. Añadir logging estructurado en backend para seguimiento de consultas y errores de API.
3. Implementar monitoreo basico: metricas de latencia, tasa de error de Gemini, tamaño de vector store.
4. Documentar procedimientos de actualizacion del curriculum y regeneracion de embeddings.

## 8. Despliegue
1. Crear Dockerfiles para backend, frontend y worker (si se usa Celery) y orquestar via docker-compose para local.
2. Definir pipeline de build y push a registro de contenedores.
3. Seleccionar plataforma (por ejemplo, backend en Render/Heroku, frontend en Streamlit Cloud o Vercel con iframe) y preparar configuraciones.
4. Establecer gestion de secretos en la plataforma elegida (RNF-005).
5. Ejecutar smoke tests post-despliegue verificando endpoints y UI.

## 9. Documentacion y soporte continuo
1. Actualizar `README` con instrucciones de instalacion, comandos clave y variables de entorno.
2. Mantener documentacion en `docs/` sobre pipeline RAG, flujos de despliegue y guias de resolucion de problemas.
3. Planificar mejoras futuras: soporte multilingue, almacenamiento persistente de sesiones, integracion analitica.
