## Stack
Frontend: Streamlit
Backend: FastAPI
DB: NoSQL (v2)
Vector DB: FAISS (v2)
LLM: OpenAI GPT-4

## Versiones

### v1
- **Frontend:** Streamlit para capturar las preferencias del usuario.
- **Backend:** FastAPI para manejar las solicitudes.
- **Llamadas a APIs externas:** Para obtener información necesaria sobre películas.
- **LLM:** Uso de OpenAI GPT-4 para procesar las preferencias del usuario y generar recomendaciones.

### v2
- **Base de datos NoSQL:** Para almacenar información de usuarios y preferencias.
- **Base de datos vectorial:** FAISS para realizar búsquedas rápidas y eficientes de películas basadas en similitudes.
- **Integración completa:** Conversaciones con la base de datos y vector DB para enriquecer las recomendaciones.