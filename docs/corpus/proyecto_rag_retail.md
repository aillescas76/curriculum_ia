# Caso de estudio: Plataforma operativa para servicios financieros retail

## Resumen
Documento de referencia sobre la modernización de las aplicaciones internas de cambio de divisas en Ebury, adoptado como base para diseñar asistentes RAG orientados a equipos de operaciones retail. Contiene contexto funcional, responsabilidades y aprendizajes reutilizables.

## Contexto
- **Empresa:** Ebury (Málaga, 2014-2021).
- **Dominio:** Operaciones de cambio de divisas B2B con necesidades de soporte 24/7.
- **Objetivo:** Mejorar la eficiencia de los procesos internos, reducir tiempos de respuesta y asegurar calidad de datos para los equipos de treasury y compliance.

## Responsabilidades de Antonio Illescas
1. **Análisis y entrega de funcionalidades**: trabajó desde la identificación de requisitos con stakeholders hasta la implementación en producción, priorizando impacto operativo.
2. **Mantenimiento evolutivo**: garantizó la continuidad del servicio, resolviendo incidencias y aplicando refactors progresivos en módulos críticos.
3. **Mentoría y code ownership**: acompañó a nuevos integrantes del equipo, revisó pull requests y estableció estándares de calidad.

## Arquitectura técnica
- **Backend principal:** Python + Django.
- **Procesamiento diferido:** Celery + Redis.
- **Base de datos:** PostgreSQL con procedimientos para conciliación de operaciones.
- **Infraestructura:** AWS (servicios gestionados para base de datos, colas y despliegues), Docker para entornos reproducibles.
- **Integraciones externas:** SendGrid para notificaciones, APIs internas de cambio.

## Resultados
- Ciclos de lanzamiento regulares con incidentes mínimos gracias al enfoque de revisión de código y pruebas continuas.
- Mayor velocidad en la incorporación de nuevos desarrolladores mediante documentación y sesiones de transferencia de conocimiento.
- Base funcional sólida para evolucionar hacia capacidades RAG (los flujos ya estructuran datos clave y mantienen trazabilidad por operación).

## Lecciones aplicables a proyectos RAG
1. **Estructuración de datos**: el modelado en Django facilitó aislar entidades y relaciones utilizadas en prompts contextuales.
2. **Procesos asíncronos**: la experiencia con Celery/Redis permite orquestar pipelines de ingestión y actualización de embeddings.
3. **Gobernanza de calidad**: la cultura de code ownership reduce riesgo de deriva en sistemas conversacionales.
4. **Segregación de responsabilidades**: separar lógica de dominio, tareas batch y servicios de soporte simplifica incorporar un vector store.

## Próximos pasos sugeridos
- Documentar taxonomía de entidades clave (clientes, divisas, límites) para convertirla en metadatos durante la ingestión.
- Identificar fuentes textuales (manuales, playbooks) que complementen el currículum y aporten contexto a un asistente RAG para equipos retail.
