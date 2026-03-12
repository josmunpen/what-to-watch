# TODO

## Pendiente

### Validación de parámetros en `search_movies_with_filters`

- [x] **`with_watch_monetization_types`** — Valores válidos: `flatrate`, `free`, `ads`, `rent`, `buy`. Actualmente sin validación, fallo silencioso si el LLM pasa otro valor. Opción: añadir `enum` en el YAML de la tool.
- [ ] **`with_original_language`** — El LLM genera el código ISO 639-1 libremente. TMDB lo ignora silenciosamente si es incorrecto. Opción: crear `LANGUAGE_MAP` en `tmdb_constants.py` (como ya existe para géneros y providers) y validar antes de enviar.
- [ ] **`sort_by`** — Hardcodeado a `popularity.desc`, no expuesto al LLM. Valores válidos: `popularity.desc`, `vote_average.desc`, `primary_release_date.desc`, etc. Valorar exponer con `enum` para que el agente pueda ordenar por valoración cuando el usuario pida "las mejores".
- [ ] **`genre` / `without_genres`** — Funciona (lanza `ValueError` visible al LLM), pero valorar añadir la lista de géneros válidos directamente en el YAML para que el LLM no tenga que adivinar.
- [ ] **`watch_region`** — El LLM genera el código ISO 3166-1 libremente. Existe `COUNTRY_MAP` en constants pero no se usa para este campo. Valorar usarlo para validar/resolver el valor.

### Nuevos endpoints TMDB a implementar como tools

**Alta prioridad**

- [x] **`get_movie_recommendations`** — `GET /movie/{id}/recommendations`. Caso de uso: "Algo parecido a X". Usa el algoritmo curado de TMDB, mejor calidad que `/similar`. Requiere `movie_id` (obtenible con `search_movie_by_title`).
- [ ] **`get_movie_watch_providers`** — `GET /movie/{id}/watch/providers`. Caso de uso: "¿En qué plataformas está X?".
- [ ] **`get_trending_movies`** — `GET /trending/movie/{time_window}` (`day` o `week`). Caso de uso: "¿Qué está de moda ahora?".
- [ ] **`get_movie_details`** — `GET /movie/{id}`. Detalles completos: runtime, tagline, colección, etc.
- [ ] **`get_similar_movies`** — `GET /movie/{id}/similar`. Complementa a `recommendations`, algoritmo por keywords/géneros.
- [ ] **`get_now_playing_movies`** — `GET /movie/now_playing`. Caso de uso: "¿Qué hay en cines ahora?".

**Media prioridad**

- [ ] **`search_person` + `get_person_movie_credits`** — `GET /search/person` + `GET /person/{id}/movie_credits`. Caso de uso: "Películas de Villeneuve" / "con Cate Blanchett". Son dos llamadas encadenadas.
- [ ] **`get_movie_credits`** — `GET /movie/{id}/credits`. Saber quién dirige/actúa en una peli concreta.
- [ ] **`get_top_rated_movies`** — `GET /movie/top_rated`. Caso de uso: "Las mejores películas de todos los tiempos".
- [ ] **`get_upcoming_movies`** — `GET /movie/upcoming`. Caso de uso: "¿Qué sale pronto?".
- [ ] **`search_movies_by_keyword`** — `GET /search/keyword` + `GET /keyword/{id}/movies`. Búsqueda por concepto (e.g. "time travel", "heist").

### Arquitectura del agente

- [ ] **Discutir el enfoque de function calling actual** — Revisar si el esquema actual (YAMLs con OpenAI Function Calling vía SDK) es el más adecuado: estructura de los schemas, cómo se pasan al LLM, si conviene migrar a otro formato o añadir validación de outputs con Pydantic, etc.
- [ ] **Evaluar PydanticAI** — Discutir para qué sirve PydanticAI y si tiene sentido adoptarlo en este proyecto: qué aporta frente al enfoque actual (OpenAI SDK + YAMLs), cuándo es útil, y si encaja con la arquitectura ReAct que estamos usando.

## En progreso

## Completado
