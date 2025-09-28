"""Streamlit entrypoint for the Curriculum Interactivo con IA UI."""
from __future__ import annotations

import os
from typing import Any, Dict, List

import requests
import streamlit as st

DEFAULT_BACKEND_BASE_URL = os.environ.get("BACKEND_BASE_URL", "http://localhost:8000")

if "backend_base_url" not in st.session_state:
    st.session_state.backend_base_url = DEFAULT_BACKEND_BASE_URL

BACKEND_HELP = (
    "API base del backend Django. Modifica este valor si ejecutas la UI contra "
    "otro host o puerto."
)

st.set_page_config(page_title="Curriculum Interactivo con IA", layout="wide")
st.title("Curriculum Interactivo con IA")

st.write(
    "Explora el perfil profesional y conversa con un asistente que pronto "
    "responderá usando RAG sobre el currículum."
)

with st.sidebar:
    st.header("Configuración")
    backend_input = st.text_input(
        "Backend URL",
        value=st.session_state.backend_base_url,
        help=BACKEND_HELP,
    )
    st.session_state.backend_base_url = backend_input or DEFAULT_BACKEND_BASE_URL

    st.header("Descarga del CV")
    st.write(
        "Mientras integramos el PDF definitivo, puedes descargar esta versión "
        "resumen en texto."
    )
    SAMPLE_CV_TEXT = (
        "Curriculum Vitae\n"
        "=================\n\n"
        "Nombre: Jane Doe\n"
        "Rol: Ingeniera de Datos e IA\n"
        "Experiencia: 7+ años en proyectos de analítica, MLOps y RAG.\n"
    )
    st.download_button(
        label="Descargar CV (TXT)",
        file_name="cv_resumen.txt",
        mime="text/plain",
        data=SAMPLE_CV_TEXT,
    )

left_col, right_col = st.columns([2, 3])

with left_col:
    st.subheader("Resumen del perfil")
    st.markdown(
        """
        **Jane Doe** — Ingeniera de Datos e IA

        - Especialista en sistemas RAG, pipelines de datos en tiempo real y despliegues en la nube.
        - Experiencia liderando equipos multidisciplinares y colaborando con stakeholders técnicos.
        - Stack principal: Python, Django, LangChain, Google Gemini, FAISS, Spark, Kubernetes.
        """
    )

    st.subheader("Logros destacados")
    st.markdown(
        """
        - Implementación de un asistente conversacional con RAG para soporte interno (reducción de tiempos de respuesta en 45%).
        - Migración de pipelines batch a streaming con Spark y Kafka (mejora de frescura de datos a <5 minutos).
        - Diseño de estrategia MLOps basada en GitOps, con despliegues canary y monitorización proactiva.
        """
    )

    st.subheader("Educación")
    st.markdown(
        """
        - M.Sc. Inteligencia Artificial, Universidad Politécnica.
        - B.Sc. Ingeniería Informática, Universidad Estatal.
        """
    )

with right_col:
    st.subheader("Chat con el asistente")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hola, soy el asistente del currículum. Pregúntame sobre experiencia, "
                    "habilidades o proyectos. En las próximas iteraciones responderé con RAG."
                ),
            }
        ]

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Escribe tu pregunta")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        placeholder = st.chat_message("assistant")
        placeholder.markdown("Estoy pensando...")

        history_payload: List[Dict[str, str]] = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.chat_history[:-1]
        ]

        endpoint = f"{st.session_state.backend_base_url.rstrip('/')}/api/chat/"

        try:
            payload: Dict[str, Any] = {
                "message": prompt,
                "history": history_payload,
            }
            response = requests.post(endpoint, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            answer = data.get(
                "reply",
                "No recibí respuesta del backend en el formato esperado.",
            )
            suggestions = data.get("suggested_questions", [])
        except Exception as exc:  # pragma: no cover - interacción manual
            answer = f"No se pudo contactar al backend: {exc}"
            suggestions = []

        placeholder.empty()
        placeholder.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        if suggestions:
            with st.expander("Preguntas sugeridas"):
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")
