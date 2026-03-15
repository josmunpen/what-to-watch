"""
MCP server for TMDB movie discovery.

Run with:
    fastmcp run mcp/server.py
"""

import sys
from pathlib import Path

# Ensure the project root is in sys.path so `app` is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastmcp import FastMCP

from app.config import settings  # noqa: F401 — triggers .env load
from app.models.movie import Movie
from app.services.tmdb_constants import resolve_provider_id
from app.services.tmdb_service import tmdb_service

mcp = FastMCP("tmdb")


def _format_movies(movies: list[Movie]) -> str:
    lines = []
    for m in movies[:10]:
        year = m.release_date[:4] if m.release_date else "?"
        overview = m.overview[:150] + "..." if len(m.overview) > 150 else m.overview
        lines.append(f"- {m.title} ({year}) [score: {m.vote_average:.1f}]: {overview}")
    return "\n".join(lines) if lines else "No movies found for that genre."


@mcp.tool()
def search_movies_with_filters(
    genre: str,
    watch_region: str = "ES",
    with_watch_providers: str | None = None,
) -> str:
    """
    Busca en TMDB películas populares de un género dado.
    Úsala siempre que el usuario pida una recomendación por género.
    El género debe estar en inglés (e.g. 'horror', 'comedy', 'thriller', 'action').

    Args:
        genre: El género de película en inglés.
        watch_region: Código ISO 3166-1 del país (e.g. 'ES', 'US'). Por defecto 'ES'.
        with_watch_providers: Plataforma de streaming (e.g. 'Netflix', 'Filmin').
            Solo incluir si el usuario lo menciona explícitamente.
    """
    provider_id: int | None = None
    if with_watch_providers is not None:
        provider_id = resolve_provider_id(with_watch_providers)
        if provider_id is None:
            return (
                f"Plataforma '{with_watch_providers}' no reconocida. "
                "Busca sin filtro de plataforma."
            )
    try:
        movies = tmdb_service.discover_movies(
            genre=genre,
            watch_region=watch_region,
            with_watch_providers=provider_id,
            page=1,
        )
    except ValueError as e:
        return str(e)
    return _format_movies(movies)


if __name__ == "__main__":
    mcp.run()
