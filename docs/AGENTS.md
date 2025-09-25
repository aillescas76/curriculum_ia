# AGENTS

## Proposito
Este documento resume los agentes de IA implicados en el proyecto "Curriculum Interactivo con IA" y define responsabilidades, interfaces y restricciones para asegurar respuestas alineadas con el curriculo del candidato.

## Panorama General
- **Agente de Ingesta**: procesa el curriculo sanitizado y construye/actualiza el almacén vectorial FAISS.
- **Agente de Recuperacion**: recibe embeddings de las consultas y devuelve fragmentos relevantes desde FAISS.
- **Agente de Conversacion**: orquesta el flujo RAG, genera las respuestas en streaming usando Gemini y mantiene el contexto.
- **Agente de Observabilidad (opcional)**: registra métricas, latencia y errores para el monitoreo continuo.

## Responsabilidades Clave
- Agente de Ingesta
  - Validar formato del documento de origen (PDF/Markdown) y versionarlo.
  - Fragmentar contenido en chunks, calcular embeddings y persistirlos.
  - Ejecutarse bajo demanda o pipeline CI cuando cambie el curriculo.
- Agente de Recuperacion
  - Servir consultas de similitud usando FAISS con un SLA < 150 ms por búsqueda.
  - Exponer interfaz clara (método/endpoint) para que el agente conversacional pueda reutilizarlo.
- Agente de Conversacion
  - Aplicar memoria conversacional limitada a la sesión en curso.
  - Interceptar preguntas fuera de alcance y responder conforme a FR-009.
  - Gestionar tokens de API y fallback en caso de errores temporales.
- Agente de Observabilidad
  - Emitir eventos de latencia, errores de la API de Gemini y ratio de recurrencia de preguntas.
  - Integrarse con la solución de logs elegida (p. ej. ELK, Prometheus) sin exponer datos sensibles.

## Flujo de Datos
1. El frontend envía la pregunta y el historial al backend.
2. El agente de Conversacion solicita embeddings al servicio de embeddings (Gemini) y llama al Agente de Recuperacion.
3. El Agente de Recuperacion devuelve contexto; el agente de Conversacion construye el prompt y llama a Gemini.
4. La respuesta se transmite al usuario y el Agente de Observabilidad registra métricas clave.

## Restricciones y Guardrails
- Uso exclusivo de datos del curriculo sanitizado; preguntas externas deben recibir negativa educada.
- Manejo seguro de credenciales (`GEMINI_API_KEY` via variables de entorno).
- Registro de logs sin incluir datos personales ni preguntas sensibles.
- Cumplir con latencia de primer token < 2 s y tiempo total < 5 s para mantener experiencia fluida.

## Operativa y Mantenimiento
- Automatizar la regeneración de embeddings tras cada actualización del curriculo.
- Documentar comandos de gestión (`manage.py build_vector_store`, scripts Streamlit) en `README` y `docs/`.
- Establecer alertas cuando aumente la tasa de preguntas sin respuesta o cuando FAISS no encuentre resultados.
- Revisar prompts y plantillas periódicamente para evitar derivas o alucinaciones.

## Consideraciones Futuras
- Extender memoria conversacional entre sesiones autenticadas.
- Añadir agente de analítica que clasifique preguntas recurrentes para retroalimentar mejoras del curriculo.
- Evaluar soporte multilingüe añadiendo detección de idioma y traducción previa.
