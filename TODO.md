# TODO

## Pendiente

### Validación de parámetros en `search_movies_with_filters`

- [x] **T-001** · **`with_watch_monetization_types`** — Valores válidos: `flatrate`, `free`, `ads`, `rent`, `buy`. Actualmente sin validación, fallo silencioso si el LLM pasa otro valor. Opción: añadir `enum` en el YAML de la tool.
- [x] **T-002** · **`with_original_language`** — Creado `LANGUAGE_MAP` en `tmdb_constants.py` (EN/ES → ISO 639-1). Validación en `llm_service.py` con `resolve_language_code()` que acepta nombres e ISO codes.
- [x] **T-003** · **`sort_by`** — Expuesto al LLM como enum en el YAML con 8 valores válidos. Validación en `llm_service.py` contra `VALID_SORT_BY`. Default: `popularity.desc`.
- [x] **T-004** · **`genre` / `without_genres`** — Añadida lista completa de géneros válidos (EN + ES) en la descripción del YAML para que el LLM no tenga que adivinar.
- [x] **T-005** · **`watch_region`** — Validación en `llm_service.py` con `resolve_country_code()` que usa `COUNTRY_MAP`. Acepta nombres ('spain') e ISO codes ('ES').

### Nuevos endpoints TMDB a implementar como tools

**Alta prioridad**

- [x] **T-006** · **`get_movie_recommendations`** — `GET /movie/{id}/recommendations`. Caso de uso: "Algo parecido a X". Usa el algoritmo curado de TMDB, mejor calidad que `/similar`. Requiere `movie_id` (obtenible con `search_movie_by_title`).
- [x] **T-007** · **`get_movie_watch_providers`** — `GET /movie/{id}/watch/providers`. Caso de uso: "¿En qué plataformas está X?".
- [x] **T-008** · **`get_trending_movies`** — `GET /trending/movie/{time_window}` (`day` o `week`). Caso de uso: "¿Qué está de moda ahora?".
- [x] **T-009** · **`get_movie_details`** — `GET /movie/{id}`. Detalles completos: runtime, tagline, colección, etc.
- [x] **T-010** · **`get_similar_movies`** — `GET /movie/{id}/similar`. Complementa a `recommendations`, algoritmo por keywords/géneros.
- [x] **T-011** · **`get_now_playing_movies`** — `GET /movie/now_playing`. Caso de uso: "¿Qué hay en cines ahora?".

**Media prioridad**

- [ ] **T-012** · **`search_person` + `get_person_movie_credits`** — `GET /search/person` + `GET /person/{id}/movie_credits`. Caso de uso: "Películas de Villeneuve" / "con Cate Blanchett". Son dos llamadas encadenadas.
- [ ] **T-013** · **`get_movie_credits`** — `GET /movie/{id}/credits`. Saber quién dirige/actúa en una peli concreta.
- [ ] **T-014** · **`get_top_rated_movies`** — `GET /movie/top_rated`. Caso de uso: "Las mejores películas de todos los tiempos".
- [ ] **T-015** · **`get_upcoming_movies`** — `GET /movie/upcoming`. Caso de uso: "¿Qué sale pronto?".
- [ ] **T-016** · **`search_movies_by_keyword`** — `GET /search/keyword` + `GET /keyword/{id}/movies`. Búsqueda por concepto (e.g. "time travel", "heist").

### Despliegue del backend en Koyeb

- [ ] **T-017** · **Crear Dockerfile** — Dockerfile multi-stage con `python:3.11-slim` + `.dockerignore`. Comando de inicio: `uvicorn main:app --host 0.0.0.0 --port 8000`.
- [ ] **T-018** · **Configurar secrets en Koyeb** — Mapear variables de `.env` (`TMDB_API_KEY`, `OPENAI_API_KEY`, `LANGSMITH_API_KEY`, etc.) como secrets en Koyeb.
- [ ] **T-019** · **Ajustar CORS y config para producción** — Permitir dominio de Koyeb en CORS. Verificar que `pydantic-settings` funcione sin archivo `.env` (solo env vars).
- [ ] **T-020** · **Desplegar en Koyeb** — Conectar repo GitHub, configurar instancia free (512MB RAM, 0.1 vCPU), puerto 8000, secrets y deploy.
- [ ] **T-021** · **Verificar deploy y health check** — Crear endpoint `/health`, probar `POST /chat` desde exterior, validar conexiones a TMDB y OpenAI.

### Arquitectura del agente

- [ ] **T-022** · **Discutir el enfoque de function calling actual** — Revisar si el esquema actual (YAMLs con OpenAI Function Calling vía SDK) es el más adecuado: estructura de los schemas, cómo se pasan al LLM, si conviene migrar a otro formato o añadir validación de outputs con Pydantic, etc.
- [ ] **T-023** · **Evaluar PydanticAI** — Discutir para qué sirve PydanticAI y si tiene sentido adoptarlo en este proyecto: qué aporta frente al enfoque actual (OpenAI SDK + YAMLs), cuándo es útil, y si encaja con la arquitectura ReAct que estamos usando.

### Testing

- [x] **T-024** · **Tests unitarios para function calls** — Testear los resolvers de `tmdb_constants.py` (`resolve_genres`, `resolve_providers`, `resolve_language_code`, `resolve_country_code`) y la validación de parámetros en `llm_service._search_movies_with_filters` (sort_by inválido, idioma no reconocido, región inválida, género desconocido, monetización inválida). Mockear `TMDBService` para aislar la lógica de validación.
- [ ] **T-025** · **Tests unitarios para tools nuevas** — Testear los wrappers de `llm_service.py` para cada tool: `_get_trending_movies` (validación de time_window), `_get_movie_details` (formateo de detalles), `_get_similar_movies`, `_get_movie_recommendations`, `_get_movie_watch_providers` (validación de región, formateo de providers), `_get_now_playing_movies` (validación de región). Mockear `TMDBService`.

### Revisión de tools

- [ ] **T-026** · **Revisar `get_similar_movies`** — Actualmente no se usa nunca porque `get_movie_recommendations` cubre el mismo caso de uso ("algo parecido a X"). Decidir si eliminarla, diferenciar mejor los prompts de ambas tools para que el LLM elija según contexto, o fusionarlas en una sola tool que combine ambos resultados.
- [ ] **T-027** · **Revisar `get_trending_movies`** — Posible solapamiento con `get_now_playing_movies`. Verificar si trending ya cubre el caso de "en cartelera" o si aportan datos distintos (trending = popularidad online vs now_playing = cartelera real). Decidir si mantener ambas o consolidar.

### UX / Registro de usuario

**Baja prioridad**

- [ ] **T-028** · **Selector de región en registro** — Permitir al usuario seleccionar su país/región en el formulario de registro. Actualmente `watch_region` está hardcodeado a `'ES'` como default. Cuando exista perfil de usuario, usar su región configurada en lugar del default.

## En progreso

## Completado
