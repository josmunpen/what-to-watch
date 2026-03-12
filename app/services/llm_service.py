import json
from pathlib import Path

import yaml
from loguru import logger
from openai import OpenAI

from app.config import settings
from app.models.movie import Movie
from app.services.tmdb_service import (
    TMDBService,
    resolve_genre_id,
    resolve_provider_id,
    tmdb_service,
)

VALID_MONETIZATION_TYPES = {"flatrate", "free", "ads", "rent", "buy"}

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
        }

    def _resolve_providers(self, names: list[str]) -> str | None:
        """Resolve a list of provider names to a pipe-separated string of IDs."""
        ids = []
        unknown = []
        for name in names:
            pid = resolve_provider_id(name)
            if pid is None:
                unknown.append(name)
            else:
                ids.append(str(pid))
        if unknown:
            unknown_str = ", ".join(unknown)
            msg = f"Plataforma(s) no reconocida(s): {unknown_str}. Busca sin filtro de plataforma."
            return None, msg
        return "|".join(ids), None

    def _resolve_genres(self, names: list[str]) -> tuple[str | None, str | None]:
        """Resolve a list of genre names to a pipe-separated string of IDs."""
        ids = []
        unknown = []
        for name in names:
            gid = resolve_genre_id(name)
            if gid is None:
                unknown.append(name)
            else:
                ids.append(str(gid))
        if unknown:
            return None, f"Género(s) no reconocido(s): {', '.join(unknown)}."
        return "|".join(ids), None

    def _search_movies_with_filters(
        self,
        genre: str | None = None,
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
    ) -> str:
        logger.debug(f"Tool called: search_movies_with_filters(genre={genre}, ...)")

        providers_str: str | None = None
        if with_watch_providers:
            providers_str, err = self._resolve_providers(with_watch_providers)
            if err:
                return err

        without_genres_str: str | None = None
        if without_genres:
            without_genres_str, err = self._resolve_genres(without_genres)
            if err:
                return err

        if with_watch_monetization_types and with_watch_monetization_types not in VALID_MONETIZATION_TYPES:
            valid = ", ".join(sorted(VALID_MONETIZATION_TYPES))
            return (
                f"Tipo de monetización no válido: '{with_watch_monetization_types}'."
                f" Valores válidos: {valid}."
            )

        try:
            movies = self._tmdb.discover_movies(
                genre=genre,
                watch_region=watch_region,
                with_watch_providers=providers_str,
                primary_release_year=primary_release_year,
                release_date_gte=release_date_gte,
                release_date_lte=release_date_lte,
                vote_average_gte=vote_average_gte,
                vote_count_gte=vote_count_gte,
                with_original_language=with_original_language,
                runtime_gte=runtime_gte,
                runtime_lte=runtime_lte,
                with_watch_monetization_types=with_watch_monetization_types,
                without_genres=without_genres_str,
                page=1,
            )
        except ValueError as e:
            return str(e)
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
