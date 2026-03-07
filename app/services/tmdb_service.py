"""
TMDB API connector.

Uses the TMDB v3 REST API with a Bearer token (API Read Access Token).
Genre IDs are stored statically – they have been stable for years.
"""

from typing import Any

import httpx

from app.config import settings
from app.models.movie import Movie
from app.services.tmdb_constants import COUNTRY_MAP, GENRE_MAP

# Reverse map for display purposes
_ID_TO_GENRE: dict[int, str] = {v: k for k, v in GENRE_MAP.items() if k != "sci-fi"}


def resolve_genre_id(genre: str) -> int | None:
    """Return the TMDB genre ID for a genre name, or None if unknown."""
    return GENRE_MAP.get(genre.lower().strip())


class TMDBService:
    """Persistent TMDB client — one httpx.Client shared across all requests."""

    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=settings.tmdb_base_url,
            timeout=10.0,
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_key}",
                "accept": "application/json",
            },
        )

    def close(self) -> None:
        self._client.close()

    def discover_movies(
        self,
        genre: str | None = None,
        country: str | None = None,
        page: int = 1,
        language: str = "en-US",
        sort_by: str = "popularity.desc",
    ) -> list[Movie]:
        """
        Query TMDB /discover/movie filtered by genre and optionally by country of origin.

        Raises:
            ValueError  – if the genre or country name is not recognised.
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        genre_id: int | None = None
        if genre is not None:
            genre_id = resolve_genre_id(genre)
            if genre_id is None:
                available = ", ".join(sorted(set(GENRE_MAP.keys())))
                raise ValueError(f"Unknown genre '{genre}'. Available genres: {available}")

        country_code: str | None = None
        if country is not None:
            country_code = COUNTRY_MAP.get(country.lower().strip())
            if country_code is None:
                available = ", ".join(sorted(set(COUNTRY_MAP.keys())))
                raise ValueError(f"Unknown country '{country}'. Available countries: {available}")

        params: dict[str, Any] = {
            "sort_by": sort_by,
            "language": language,
            "page": page,
        }
        if genre_id is not None:
            params["with_genres"] = genre_id
        if country_code is not None:
            params["watch_region"] = country_code

        response = self._client.get("/discover/movie", params=params)
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


# Singleton — created once when the module is first imported
tmdb_service = TMDBService()


def get_tmdb_service() -> TMDBService:
    """FastAPI dependency that returns the shared TMDBService instance."""
    return tmdb_service
