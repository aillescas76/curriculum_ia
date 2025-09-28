# Caso de estudio: Migración progresiva a nube gestionada

## Resumen
Relato de la experiencia de Antonio Illescas liderando evoluciones cloud-native en proyectos donde convivían cargas on-premise y servicios gestionados, con énfasis en plataformas Django y automatización backend.

## Contexto principal
- **Organizaciones:** Mr. Milu (2023-actualidad) y Ebury (2014-2021).
- **Motivación:** Escalar aplicaciones críticas sin degradar disponibilidad, habilitar despliegues rápidos y optimizar costes operativos.

## Enfoque adoptado
1. **Contenerización con Docker** para homogeneizar entornos de desarrollo, staging y producción.
2. **Servicios gestionados en AWS** (PostgreSQL, colas, almacenamiento) para reducir carga de mantenimiento.
3. **Automatización con Celery y Redis** para procesar tareas de larga duración fuera del request/response.
4. **Observabilidad básica** mediante logs centralizados y monitoreo del rendimiento tras cada iteración.

## Rol de Antonio Illescas
- Diseño de pipelines de despliegue en coordinación con equipos frontend y QA.
- Refactorización de componentes monolíticos en Django para facilitar el empaquetado y el escalado horizontal.
- Coordinación con stakeholders técnicos para planificar ventanas de migración y estrategias de rollback.
- Documentación práctica para nuevos desarrolladores sobre cómo levantar entornos en la nube.

## Resultados logrados
- Reducción del tiempo de entrega de nuevas funcionalidades al disponer de infra reproducible.
- Mayor resiliencia frente a picos de tráfico gracias a colas asíncronas y balanceo en AWS.
- Facilitación del trabajo remoto al contar con pipelines y entornos autodescriptivos.

## Relación con el proyecto RAG
- La infraestructura Docker + AWS sirve para alojar servicios de ingestión y APIs de recuperación.
- Experiencia previa con Redis allana la incorporación de memorias conversacionales y colas para procesamiento de embeddings.
- Los procedimientos de despliegue controlado se reutilizan para lanzar nuevos índices FAISS sin interrumpir al usuario.

## Recomendaciones futuras
- Añadir monitoreo específico de latencia de consultas al vector store.
- Evaluar infraestructura gestionada para FAISS (p.ej. instancias dedicadas con backups automatizados).
- Integrar pruebas de carga en CI/CD para validar escalado del chat antes de despliegues.
