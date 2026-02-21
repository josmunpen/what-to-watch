# What to Watch

## Instrucciones para levantar el proyecto

Este proyecto incluye un backend desarrollado con FastAPI y un frontend sencillo con Streamlit. A continuación, se detallan los pasos para levantar ambos servicios.

---

## **Requisitos previos**

1. **Python 3.9 o superior** instalado.
2. Crear y activar un entorno virtual:

   - En **PowerShell**:
     ```powershell
     python -m venv env_wtw
     .\env_wtw\Scripts\Activate
     ```

   - En **CMD**:
     ```cmd
     python -m venv env_wtw
     .\env_wtw\Scripts\activate
     ```

3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Levantar el backend**

1. Asegúrate de estar en el directorio raíz del proyecto.
2. Ejecuta el siguiente comando para iniciar el servidor FastAPI:
   ```bash
   uvicorn main:app --reload
   ```
3. El backend estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## **Levantar el frontend**

1. En una nueva terminal (con el entorno virtual activado), ejecuta:
   ```bash
   streamlit run frontend.py
   ```
2. El frontend estará disponible en: [http://localhost:8501](http://localhost:8501)

---

## **Notas adicionales**

- Asegúrate de que el backend esté corriendo antes de iniciar el frontend.
- Si necesitas detener el backend o el frontend, usa `Ctrl + C` en la terminal correspondiente.

¡Listo! Ahora puedes interactuar con el sistema para obtener recomendaciones de películas.