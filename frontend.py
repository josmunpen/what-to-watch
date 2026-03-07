import os

import requests
import streamlit as st
from streamlit_chat import message as st_message

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("What to Watch")

st.write("Habla con el sistema para obtener recomendaciones de películas.")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    st_message(msg["content"], is_user=msg["is_user"])

# Input for user message
user_input = st.text_input("Escribe tu mensaje aquí:", key="user_input")

if st.button("Enviar"):
    if user_input:
        # Add user message to chat history
        st.session_state["messages"].append({"content": user_input, "is_user": True})

        # Build history (previous messages, excluding the one just added)
        history = [
            {"role": "user" if msg["is_user"] else "assistant", "content": msg["content"]}
            for msg in st.session_state["messages"][:-1]
        ]

        # Send user message to backend
        response = requests.post(f"{BACKEND_URL}/chat", json={"message": user_input, "history": history})
        if response.status_code == 200:
            recommendation_response = response.json().get("response", "No se pudo obtener una respuesta.")
            # Add system response to chat history
            st.session_state["messages"].append({"content": recommendation_response, "is_user": False})
            # Ensure the system message is rendered correctly
            st_message(recommendation_response, is_user=False)
        else:
            st.error("Error al obtener recomendaciones.")
    else:
        st.warning("Por favor, escribe un mensaje.")