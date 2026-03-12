import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("What to Watch")
st.caption("Habla con el sistema para obtener recomendaciones de películas.")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    role = "user" if msg["is_user"] else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# Chat input (fixed at the bottom)
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Show and store user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state["messages"].append({"content": prompt, "is_user": True})

    # Build history (excluding the message just added)
    history = [
        {"role": "user" if msg["is_user"] else "assistant", "content": msg["content"]}
        for msg in st.session_state["messages"][:-1]
    ]

    # Call backend and show response
    with st.chat_message("assistant"):
        with st.spinner("Buscando recomendaciones..."):
            response = requests.post(
                f"{BACKEND_URL}/chat", json={"message": prompt, "history": history}
            )
        if response.status_code == 200:
            reply = response.json().get("response", "No se pudo obtener una respuesta.")
            st.markdown(reply)
            st.session_state["messages"].append({"content": reply, "is_user": False})
        else:
            st.error("Error al obtener recomendaciones.")
