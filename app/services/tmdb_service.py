"""
TMDB API connector.

Uses the TMDB v3 REST API with a Bearer token (API Read Access Token).
Genre IDs are stored statically – they have been stable for years.
"""

from dataclasses import dataclass
from typing import Any
import httpx
from app.config import settings

# ---------------------------------------------------------------------------
# Static genre map  (TMDB movie genre IDs, as of 2025)
# Source: https://api.themoviedb.org/3/genre/movie/list
# ---------------------------------------------------------------------------
GENRE_MAP: dict[str, int] = {
    # English
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "science fiction": 878,
    "sci-fi": 878,
    "thriller": 53,
    "tv movie": 10770,
    "war": 10752,
    "western": 37,
    # Spanish aliases
    "acción": 28,
    "accion": 28,
    "aventura": 12,
    "animación": 16,
    "animacion": 16,
    "comedia": 35,
    "crimen": 80,
    "documental": 99,
    "drama": 18,
    "familia": 10751,
    "fantasía": 14,
    "fantasia": 14,
    "historia": 36,
    "terror": 27,
    "música": 10402,
    "musica": 10402,
    "misterio": 9648,
    "romance": 10749,
    "ciencia ficción": 878,
    "ciencia ficcion": 878,
    "bélico": 10752,
    "belico": 10752,
    "guerra": 10752,
    "oeste": 37,
}

# Reverse map for display purposes
_ID_TO_GENRE: dict[int, str] = {v: k for k, v in GENRE_MAP.items() if k != "sci-fi"}


@dataclass(slots=True)
class Movie:
    """Simple domain object for TMDB movies."""

    id: int
    title: str
    overview: str
    release_date: str
    vote_average: float
    genre_ids: list[int]


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {settings.tmdb_api_key}",
        "accept": "application/json",
    }


def resolve_genre_id(genre_name: str) -> int | None:
    """Return the TMDB genre ID for a genre name, or None if unknown."""
    return GENRE_MAP.get(genre_name.lower().strip())


def discover_movies_by_genre(
    genre_name: str,
    *,
    page: int = 1,
    language: str = "en-US",
    sort_by: str = "popularity.desc",
) -> list[Movie]:
    """
    Query TMDB /discover/movie filtered by genre.

    Returns a list of movie dicts with keys:
        id, title, overview, release_date, vote_average, genre_ids

    Raises:
        ValueError  – if the genre name is not recognised.
        httpx.HTTPStatusError – on non-2xx responses from TMDB.
    """
    genre_id = resolve_genre_id(genre_name)
    if genre_id is None:
        available = ", ".join(sorted(set(GENRE_MAP.keys())))
        raise ValueError(
            f"Unknown genre '{genre_name}'. Available genres: {available}"
        )

    params: dict[str, Any] = {
        "with_genres": genre_id,
        "sort_by": sort_by,
        "language": language,
        "page": page,
    }

    with httpx.Client(base_url=settings.tmdb_base_url, timeout=10.0) as client:
        response = client.get("/discover/movie", headers=_headers(), params=params)
        response.raise_for_status()

    results: list[dict[str, Any]] = response.json().get("results", [])
    return [
        Movie(
            id=movie["id"],
            title=movie["title"],
            overview=movie.get("overview", ""),
            release_date=movie.get("release_date", ""),
            vote_average=movie.get("vote_average", 0.0),
            genre_ids=movie.get("genre_ids", []),
        )
        for movie in results
    ]