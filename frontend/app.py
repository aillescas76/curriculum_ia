"""Streamlit entrypoint for the Curriculum Interactivo con IA UI."""
from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

BACKEND_BASE_URL = os.environ.get("BACKEND_BASE_URL", "http://backend:8000")
CHAT_ENDPOINT = f"{BACKEND_BASE_URL.rstrip('/')}/chat/"

st.set_page_config(page_title="Curriculum Interactivo con IA", layout="wide")

st.title("Curriculum Interactivo con IA")
st.write(
    "Interactúa con el currículum del candidato a través de un chatbot impulsado por IA."
)

with st.sidebar:
    st.header("Descarga del CV")
    st.write("Una versión PDF estará disponible en futuras iteraciones.")
    st.header("Configuración")
    st.text_input("Backend URL", value=BACKEND_BASE_URL, disabled=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hola, soy el asistente del currículum. Pregúntame sobre experiencia, "
                "habilidades o proyectos destacados."
            ),
        }
    ]

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    placeholder = st.chat_message("assistant")
    placeholder.markdown("Estoy pensando...")

    try:
        payload: dict[str, Any] = {"question": prompt, "history": st.session_state.chat_history}
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "No recibí respuesta del backend.")
    except Exception as exc:  # pragma: no cover - interacción manual
        answer = f"No se pudo contactar al backend: {exc}"

    placeholder.empty()
    placeholder.markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
