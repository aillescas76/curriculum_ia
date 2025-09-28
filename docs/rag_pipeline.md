# Pipeline RAG: Ingesta y Recuperación

Este documento describe cómo implementar el flujo RAG (Retrieval-Augmented Generation) del proyecto "Curriculum Interactivo con IA". Incluye los pasos necesarios para preparar el vector store offline y el proceso online que usa Django + LangChain para responder preguntas con contexto.

## 1. Conceptos clave
- **Vector store**: índice FAISS persistido en `vectorstore-data/` que almacena embeddings del currículum y documentos complementarios.
- **Embeddings**: representaciones numéricas generadas con la API de Google Gemini (`models/embedding-001` o similar).
- **Chunks**: fragmentos de texto (300-500 tokens) que balancean precisión y límite de contexto.
- **Retriever**: componente LangChain que realiza búsquedas de similitud y devuelve los mejores fragmentos.
- **LLM**: modelo conversacional (p. ej. `gemini-1.5-flash`) que recibe la pregunta, contexto recuperado y la memoria de la conversación.

## 2. Ingesta offline

### 2.1 Preparación del entorno
1. **Documentos sanitizados**: ubicar PDFs o Markdown en `docs/corpus/`. Cumplir RNF-004 (sin datos sensibles).
2. **Variables de entorno** (agregar a `.env` y `docs/.env.example`):
   - `GEMINI_API_KEY`
   - `VECTORSTORE_DIR=vectorstore-data`
   - `EMBEDDING_MODEL=embedding-001`
   - `CHUNK_SIZE=500`
3. Instalar dependencias necesarias (`pip install -e .[dev]`): LangChain, google-generativeai, pypdf, faiss-cpu, etc.

### 2.2 Arquitectura de ingestión
```
manage.py build_vector_store
└── ingest/__init__.py             # Interfaces comunes
    ├── loader.py                  # Convierte PDF/MD a texto normalizado
    ├── chunker.py                 # Aplica splitters (LangChain RecursiveTextSplitter)
    ├── embeddings.py              # Envuelve llamadas a Gemini
    └── persistence.py             # Crea/actualiza el índice FAISS
```

### 2.3 Flujo paso a paso
1. **Cargar documento**
   - Detectar tipo (PDF/MD/HTML ligero).
   - Usar pypdf o markdown parser para obtener texto plano.
2. **Normalizar y dividir**
   - Eliminar encabezados repetidos/espacios.
   - `RecursiveCharacterTextSplitter` con `chunk_size` y `chunk_overlap` (~80 tokens).
   - Añadir metadatos: `document_id`, `title`, `page`, `section`.
3. **Generar embeddings**
   - Inicializar `GoogleGenerativeAIEmbeddings` con la API key.
   - Reintentar 3 veces en caso de 429/5xx.
4. **Persistir vector store**
   - Para primera ejecución: `FAISS.from_texts(texts, embeddings, metadatas=...)`.
   - Para actualizaciones: cargar índice existente y llamar `index.add_embeddings(...)`.
   - Guardar en `vectorstore-data/{document_id}` usando `faiss.write_index` + pickle de metadatos.
5. **Command** `build_vector_store`
   - Argumentos: `--source <ruta>`, `--document-id <slug>`, `--rebuild`.
   - Opción `--dry-run` para imprimir métricas sin escribir.
   - Registrar métricas: nº de chunks, tamaño índice, tiempo total.

### 2.4 Pruebas de ingestión
- Test unitario `tests/ingest/test_chunker.py`: asegura que el splitter respeta tamaño y overlap.
- Test `tests/ingest/test_embeddings.py`: valida que se generen vectores (mock API).
- Test integración `tests/ingest/test_command.py`: ejecuta comando sobre fixture Markdown y verifica archivos en `vectorstore-data/`.

## 3. Recuperación online

### 3.1 Componentes en Django
```
backend/chat/
├── services/
│   ├── retrieval.py      # Carga vector store y ejecuta similitud
│   ├── generator.py      # Orquesta prompt + llamada a Gemini chat
│   ├── memory.py         # Administra historial (LangChain ConversationBuffer)
│   └── prompts.py        # Plantillas con instrucciones y formato de cita
├── views.py              # Recibe POST /api/chat/
└── serializers.py        # Valida entrada/salida
```

### 3.2 Flujo de una pregunta
1. **Validación** `ChatRequestSerializer` recibe `message` + `history`.
2. **Embeddings de consulta**: `GoogleGenerativeAIEmbeddings.embed_query(message)`.
3. **Búsqueda FAISS**: `retriever.get_relevant_documents(query, k=4)`. Aplicar score threshold para ruido.
4. **Construcción del prompt**
   - Prompt base + secciones ancladas con citas `[{doc_id}:{chunk_id}]`.
   - Incluir instrucciones RNF-004/OOS (si no hay contexto relevante → respuesta de límites).
5. **Generación**
   - `ChatGoogleGenerativeAI` con streaming (`stream=True` para FR-010).
   - Combinar tokens en generador y emitir vía `StreamingHttpResponse`.
6. **Respuesta**
   - Formato JSON: `reply`, `citations`, `suggested_questions`.
   - Registrar logs con metadatos (latencia, nº chunks).

### 3.3 Gestión de memoria
- Para MVP: memoria efímera por request (`history` en payload).
- Evolución: almacenar sesiones en Redis/Postgres con `session_id`.
- Long context: recapitular cada n mensajes usando resumen intermedio.

### 3.4 Manejo de preguntas fuera de alcance
- Si no hay documentos con score ≥ umbral, devolver mensaje estándar (FR-009).
- Sugerir temas válidos usando plantilla estática + metadatos del perfil.

### 3.5 Pruebas de recuperación
- Mock embeddings + vector store para evitar llamadas reales.
- `tests/chat/test_retrieval_service.py`: verifica ranking y filtrado.
- `tests/chat/test_chat_flow.py`: simula una pregunta y valida que el prompt incluya fragmentos.
- Correr `pytest backend/tests` en CI.

## 4. Operación y mantenimiento
- **Regenerar embeddings** cada vez que se actualiza el currículum o se agrega un documento nuevo.
- **Versionado**: nombrar índices `vectorstore-data/{document_id}/v{timestamp}` y mantener alias activo.
- **Monitoring**: contadores de latencia (primera token), nº de tokens por respuesta, ratio OOS.
- **Backup**: subir directorio `vectorstore-data` a almacenamiento persistente (S3, GCS) en despliegues productivos.

## 5. Próximos pasos
- Implementar `build_vector_store` con CLI robusta y logging estructurado.
- Integrar streaming real en `ChatView` usando `StreamingHttpResponse` y generadores async.
- Añadir panel de administración para recargar vector store sin reiniciar la app.
- Evaluar uso de `langchain.retrievers.ContextualCompressionRetriever` para compactar contexto si el número de documentos crece.

Mantener este documento actualizado conforme se implementen mejoras o cambien dependencias del pipeline.
