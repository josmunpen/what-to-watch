import json
from pathlib import Path

import yaml
from loguru import logger
from openai import OpenAI

from app.config import settings
from app.models.movie import Movie
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
        }

    def _search_movies_with_filters(self, genre: str) -> str:
        logger.debug(f"Tool called: search_movies_with_filters(genre={genre})")
        try:
            movies = self._tmdb.discover_movies(genre_name=genre, page=1)
        except ValueError as e:
            return str(e)
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
