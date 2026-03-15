import json
from pathlib import Path

import yaml
from loguru import logger
from openai import OpenAI

from app.config import settings
from app.models.movie import Movie
from app.services.tmdb_constants import (
    VALID_MONETIZATION_TYPES,
    VALID_SORT_BY,
    resolve_country_code,
    resolve_genres,
    resolve_language_code,
    resolve_providers,
)
from app.services.tmdb_service import TMDBService, tmdb_service

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
_TOOLS_DIR = Path(__file__).parent.parent / "tools"

SYSTEM_PROMPT = (_PROMPTS_DIR / "system_prompt.txt").read_text(encoding="utf-8")

TOOLS = [
    yaml.safe_load(path.read_text(encoding="utf-8")) for path in sorted(_TOOLS_DIR.glob("*.yaml"))
]


def _format_movies(movies: list[Movie]) -> str:
    lines = []
    for m in movies[:10]:
        year = m.release_date[:4] if m.release_date else "?"
        overview = m.overview[:150] + "..." if len(m.overview) > 150 else m.overview
        lines.append(f"- {m.title} ({year}) [score: {m.vote_average:.1f}]: {overview}")
    return "\n".join(lines) if lines else "No movies found for that genre."


class LLMService:
    """Agent wrapper — one OpenAI client shared across all requests."""

    def __init__(self, tmdb: TMDBService) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._tmdb = tmdb
        self._available_tools = {
            "search_movies_with_filters": self._search_movies_with_filters,
            "search_movie_by_title": self._search_movie_by_title,
            "get_movie_recommendations": self._get_movie_recommendations,
            "get_movie_watch_providers": self._get_movie_watch_providers,
            "get_trending_movies": self._get_trending_movies,
            "get_movie_details": self._get_movie_details,
            "get_similar_movies": self._get_similar_movies,
            "get_now_playing_movies": self._get_now_playing_movies,
        }

    def _search_movies_with_filters(
        self,
        with_genres: list[str] | None = None,
        watch_region: str = "ES",
        with_watch_providers: list[str] | None = None,
        primary_release_year: int | None = None,
        release_date_gte: str | None = None,
        release_date_lte: str | None = None,
        vote_average_gte: float | None = None,
        vote_count_gte: int | None = None,
        with_original_language: str | None = None,
        runtime_gte: int | None = None,
        runtime_lte: int | None = None,
        with_watch_monetization_types: str | None = None,
        without_genres: list[str] | None = None,
        sort_by: str = "popularity.desc",
    ) -> str:
        logger.debug("Tool called: search_movies_with_filters ...)")

        # --- Validate sort_by ---
        if sort_by not in VALID_SORT_BY:
            valid = ", ".join(sorted(VALID_SORT_BY))
            return f"sort_by no válido: '{sort_by}'. Valores válidos: {valid}."

        # --- Validate watch_region ---
        resolved_region = resolve_country_code(watch_region)
        if resolved_region is None:
            return f"Región no reconocida: '{watch_region}'. Usa un código ISO 3166-1 (e.g. 'ES', 'US') o nombre de país en inglés."

        # --- Validate with_original_language ---
        resolved_language: str | None = None
        if with_original_language:
            resolved_language = resolve_language_code(with_original_language)
            if resolved_language is None:
                return f"Idioma no reconocido: '{with_original_language}'. Usa un código ISO 639-1 (e.g. 'ko', 'fr') o nombre de idioma."

        # --- Validate included genres ---
        with_genres_str: str | None = None
        if with_genres:
            with_genres_str, err = resolve_genres(with_genres)
            if err:
                return err

        # --- Validate providers ---
        providers_str: str | None = None
        if with_watch_providers:
            providers_str, err = resolve_providers(with_watch_providers)
            if err:
                return err

        # --- Validate excluded genres ---
        without_genres_str: str | None = None
        if without_genres:
            without_genres_str, err = resolve_genres(without_genres)
            if err:
                return err

        # --- Validate monetization type ---
        if (
            with_watch_monetization_types
            and with_watch_monetization_types not in VALID_MONETIZATION_TYPES
        ):
            valid = ", ".join(sorted(VALID_MONETIZATION_TYPES))
            return (
                f"Tipo de monetización no válido: '{with_watch_monetization_types}'."
                f" Valores válidos: {valid}."
            )

        movies = self._tmdb.discover_movies(
            with_genres=with_genres_str,
            watch_region=resolved_region,
            with_watch_providers=providers_str,
            primary_release_year=primary_release_year,
            release_date_gte=release_date_gte,
            release_date_lte=release_date_lte,
            vote_average_gte=vote_average_gte,
            vote_count_gte=vote_count_gte,
            with_original_language=resolved_language,
            runtime_gte=runtime_gte,
            runtime_lte=runtime_lte,
            with_watch_monetization_types=with_watch_monetization_types,
            without_genres=without_genres_str,
            sort_by=sort_by,
            page=1,
        )
        return _format_movies(movies)

    def _search_movie_by_title(self, query: str) -> str:
        logger.debug(f"Tool called: search_movie_by_title(query={query})")
        movies = self._tmdb.search_movies(query)
        if not movies:
            return f"No se encontraron películas para la búsqueda: '{query}'."
        return _format_movies(movies)

    def _get_movie_recommendations(self, movie_id: int) -> str:
        logger.debug(f"Tool called: get_movie_recommendations(movie_id={movie_id})")
        movies = self._tmdb.get_movie_recommendations(movie_id)
        if not movies:
            return f"No se encontraron recomendaciones para la película con ID {movie_id}."
        return _format_movies(movies)

    def _get_movie_watch_providers(self, movie_id: int, watch_region: str = "ES") -> str:
        logger.debug(f"Tool called: get_movie_watch_providers(movie_id={movie_id})")

        resolved_region = resolve_country_code(watch_region)
        if resolved_region is None:
            return f"Región no reconocida: '{watch_region}'. Usa un código ISO 3166-1 (e.g. 'ES', 'US') o nombre de país en inglés."

        providers = self._tmdb.get_movie_watch_providers(movie_id, watch_region=resolved_region)
        if not providers:
            return f"No se encontraron plataformas disponibles para la película con ID {movie_id} en la región {resolved_region}."

        labels = {
            "flatrate": "Suscripción",
            "rent": "Alquiler",
            "buy": "Compra",
            "free": "Gratis",
            "ads": "Con anuncios",
        }
        lines = []
        for category, names in providers.items():
            label = labels.get(category, category)
            lines.append(f"- {label}: {', '.join(names)}")
        return "\n".join(lines)

    def _get_trending_movies(self, time_window: str = "week") -> str:
        logger.debug(f"Tool called: get_trending_movies(time_window={time_window})")
        if time_window not in ("day", "week"):
            return f"time_window no válido: '{time_window}'. Usa 'day' o 'week'."
        movies = self._tmdb.get_trending_movies(time_window)
        if not movies:
            return "No se encontraron películas en tendencia."
        return _format_movies(movies)

    def _get_movie_details(self, movie_id: int) -> str:
        logger.debug(f"Tool called: get_movie_details(movie_id={movie_id})")
        details = self._tmdb.get_movie_details(movie_id)
        if not details:
            return f"No se encontraron detalles para la película con ID {movie_id}."

        genres = ", ".join(g["name"] for g in details.get("genres", []))
        runtime = details.get("runtime", 0)
        hours, mins = divmod(runtime, 60) if runtime else (0, 0)
        budget = details.get("budget", 0)
        revenue = details.get("revenue", 0)
        collection = details.get("belongs_to_collection")
        collection_name = collection["name"] if collection else None

        lines = [
            f"**{details.get('title', '?')}** ({details.get('release_date', '?')[:4]})",
            f"- Tagline: {details.get('tagline', 'N/A')}",
            f"- Géneros: {genres}",
            f"- Duración: {hours}h {mins}min",
            f"- Puntuación: {details.get('vote_average', 0):.1f}/10 ({details.get('vote_count', 0)} votos)",
            f"- Sinopsis: {details.get('overview', 'N/A')}",
        ]
        if budget:
            lines.append(f"- Presupuesto: ${budget:,}")
        if revenue:
            lines.append(f"- Recaudación: ${revenue:,}")
        if collection_name:
            lines.append(f"- Colección: {collection_name}")
        return "\n".join(lines)

    def _get_similar_movies(self, movie_id: int) -> str:
        logger.debug(f"Tool called: get_similar_movies(movie_id={movie_id})")
        movies = self._tmdb.get_similar_movies(movie_id)
        if not movies:
            return f"No se encontraron películas similares para la película con ID {movie_id}."
        return _format_movies(movies)

    def _get_now_playing_movies(self, region: str = "ES") -> str:
        logger.debug(f"Tool called: get_now_playing_movies(region={region})")
        resolved_region = resolve_country_code(region)
        if resolved_region is None:
            return f"Región no reconocida: '{region}'. Usa un código ISO 3166-1 (e.g. 'ES', 'US') o nombre de país en inglés."
        movies = self._tmdb.get_now_playing_movies(region=resolved_region)
        if not movies:
            return f"No se encontraron películas en cartelera en la región {resolved_region}."
        return _format_movies(movies)

    def run_agent(self, user_message: str, history: list[dict] | None = None) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        while True:
            response = self._client.chat.completions.create(
                model=settings.default_model,
                messages=messages,
                tools=TOOLS,
            )

            assistant_message = response.choices[0].message
            messages.append(assistant_message)

            # No tool calls → respuesta final del LLM
            if not assistant_message.tool_calls:
                return assistant_message.content

            # Ejecutar cada tool call y añadir el resultado al historial
            for tool_call in assistant_message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                logger.debug(f"Executing tool: {name}({args})")

                result = self._available_tools[name](**args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )


# Singleton — created once when the module is first imported
llm_service = LLMService(tmdb=tmdb_service)


def get_llm_service() -> LLMService:
    """FastAPI dependency that returns the shared LLMService instance."""
    return llm_service
