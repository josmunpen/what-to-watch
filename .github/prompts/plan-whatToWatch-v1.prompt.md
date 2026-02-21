### Plan: Implementación de la Versión 1 del Proyecto "What to Watch"

Este plan detalla los pasos necesarios para implementar la versión 1 del proyecto "What to Watch", siguiendo las especificaciones descritas en los documentos adjuntos. La implementación se dividirá en cuatro fases: estructura del proyecto en FastAPI, creación de endpoints básicos, mockeo de llamadas a APIs externas, mockeo de la llamada al LLM, y finalmente, la integración de un frontend sencillo con Streamlit.

---

## **Fase 1: Estructura del Proyecto en FastAPI**

**Objetivo:** Crear la estructura base del proyecto en FastAPI para soportar los endpoints necesarios.

**Pasos:**
1. Crear la estructura básica del proyecto:
   - Carpeta raíz: `whattowatch/`
   - Subcarpetas:
     - `app/` para el código principal.
     - `app/routers/` para organizar los endpoints.
     - `app/models/` para definir modelos de datos.
     - `app/services/` para lógica de negocio y llamadas externas.
     - `tests/` para pruebas unitarias.
   - Archivo principal: `main.py` para inicializar la aplicación FastAPI.
2. Configurar el archivo `main.py` para inicializar la app y registrar los routers.
3. Crear un archivo `requirements.txt` con las dependencias iniciales:
   - `fastapi`
   - `uvicorn`
   - `httpx` (para futuras llamadas a APIs externas).

---

## **Fase 2: Endpoints Básicos**

**Objetivo:** Implementar los endpoints básicos necesarios para la funcionalidad inicial.

**Endpoints:**
1. **`/` (GET):** Endpoint de prueba para verificar que el servidor está funcionando.
2. **`/recommendations` (POST):** Recibe la consulta del usuario con sus preferencias y devuelve recomendaciones de películas/series.
   - Entrada esperada: JSON con las preferencias del usuario.
   - Salida: JSON con una lista de películas/series recomendadas (mockeadas).

**Pasos:**
1. Crear un router en `app/routers/recommendations.py` para manejar las rutas relacionadas con recomendaciones.
2. Implementar la lógica básica en `app/services/recommendation_service.py` para devolver datos mockeados.
3. Registrar el router en `main.py`.

---

## **Fase 3: Mockeo de Llamadas a APIs Externas**

**Objetivo:** Simular las llamadas a APIs externas para obtener información de películas/series.

**Pasos:**
1. Crear un servicio en `app/services/external_api_service.py` que simule las respuestas de una API de películas.
   - Ejemplo de datos mockeados: título, género, sinopsis, año de lanzamiento.
2. Integrar este servicio en el endpoint `/recommendations` para enriquecer las recomendaciones con datos simulados.

---

## **Fase 4: Mockeo de la Llamada al LLM**

**Objetivo:** Simular la interacción con el modelo de lenguaje (LLM) para procesar las preferencias del usuario.

**Pasos:**
1. Crear un servicio en `app/services/llm_service.py` que utilice el LLM para generar recomendaciones directamente.
   - Entrada: Preferencias del usuario.
   - Salida: Recomendaciones generadas en tiempo real.
2. Integrar este servicio en el endpoint `/recommendations` para devolver recomendaciones basadas en las preferencias del usuario.

---

## **Fase 5: Frontend Sencillo con Streamlit**

**Objetivo:** Crear una interfaz básica para que los usuarios interactúen con el sistema.

**Pasos:**
1. Crear un archivo `frontend.py` en la raíz del proyecto para la app de Streamlit.
2. Implementar una interfaz básica:
   - Campo de texto para que el usuario ingrese sus preferencias.
   - Botón para enviar las preferencias al backend.
   - Mostrar las recomendaciones devueltas por el backend.
3. Configurar Streamlit para ejecutarse junto con el backend FastAPI.

---

## **Verificación**

**Pruebas:**
1. Verificar que el servidor FastAPI se inicie correctamente y los endpoints respondan.
2. Probar el endpoint `/recommendations` con diferentes entradas y validar las respuestas mockeadas.
3. Validar que las simulaciones de las APIs externas y el LLM funcionen correctamente.
4. Probar la integración con Streamlit y verificar que las recomendaciones se muestren en el frontend.

---

## **Decisiones**
- Se utilizarán datos mockeados para las APIs externas y el LLM en esta versión para simplificar la implementación inicial.
- La estructura modular del proyecto permitirá una fácil transición a la versión 2, donde se integrarán bases de datos y funcionalidades avanzadas.
