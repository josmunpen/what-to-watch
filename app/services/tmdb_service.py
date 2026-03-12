"""
TMDB API connector.

Uses the TMDB v3 REST API with a Bearer token (API Read Access Token).
Genre IDs are stored statically – they have been stable for years.
"""

from typing import Any

import httpx

from app.config import settings
from app.models.movie import Movie
from app.services.tmdb_constants import GENRE_MAP, PROVIDER_MAP

# Reverse map for display purposes
_ID_TO_GENRE: dict[int, str] = {v: k for k, v in GENRE_MAP.items() if k != "sci-fi"}


def resolve_genre_id(genre: str) -> int | None:
    """Return the TMDB genre ID for a genre name, or None if unknown."""
    return GENRE_MAP.get(genre.lower().strip())


def resolve_provider_id(provider: str) -> int | None:
    """Return the TMDB provider ID for a provider name, or None if unknown."""
    return PROVIDER_MAP.get(provider.lower().strip())


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
        watch_region: str | None = None,
        with_watch_providers: str | None = None,
        primary_release_year: int | None = None,
        release_date_gte: str | None = None,
        release_date_lte: str | None = None,
        vote_average_gte: float | None = None,
        vote_count_gte: int | None = None,
        with_original_language: str | None = None,
        runtime_gte: int | None = None,
        runtime_lte: int | None = None,
        with_watch_monetization_types: str | None = None,
        without_genres: str | None = None,
        page: int = 1,
        language: str = "en-US",
        sort_by: str = "popularity.desc",
    ) -> list[Movie]:
        """
        Query TMDB /discover/movie with rich filtering options.

        Raises:
            ValueError  – if the genre name is not recognised.
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        genre_id: int | None = None
        if genre is not None:
            genre_id = resolve_genre_id(genre)
            if genre_id is None:
                available = ", ".join(sorted(set(GENRE_MAP.keys())))
                raise ValueError(f"Unknown genre '{genre}'. Available genres: {available}")

        params: dict[str, Any] = {
            "sort_by": sort_by,
            "language": language,
            "page": page,
        }
        if genre_id is not None:
            params["with_genres"] = genre_id
        if watch_region is not None:
            params["watch_region"] = watch_region
        if with_watch_providers is not None:
            params["with_watch_providers"] = with_watch_providers
        if primary_release_year is not None:
            params["primary_release_year"] = primary_release_year
        if release_date_gte is not None:
            params["primary_release_date.gte"] = release_date_gte
        if release_date_lte is not None:
            params["primary_release_date.lte"] = release_date_lte
        if vote_average_gte is not None:
            params["vote_average.gte"] = vote_average_gte
        if vote_count_gte is not None:
            params["vote_count.gte"] = vote_count_gte
        if with_original_language is not None:
            params["with_original_language"] = with_original_language
        if runtime_gte is not None:
            params["with_runtime.gte"] = runtime_gte
        if runtime_lte is not None:
            params["with_runtime.lte"] = runtime_lte
        if with_watch_monetization_types is not None:
            params["with_watch_monetization_types"] = with_watch_monetization_types
        if without_genres is not None:
            params["without_genres"] = without_genres

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

    def search_movies(
        self,
        query: str,
        page: int = 1,
        language: str = "en-US",
    ) -> list[Movie]:
        """Search movies by title using TMDB /search/movie.

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        params: dict[str, Any] = {
            "query": query,
            "page": page,
            "language": language,
        }

        response = self._client.get("/search/movie", params=params)
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


    def get_movie_recommendations(
        self,
        movie_id: int,
        page: int = 1,
        language: str = "en-US",
    ) -> list[Movie]:
        """Get curated recommendations for a movie using TMDB /movie/{id}/recommendations.

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        params: dict[str, Any] = {"page": page, "language": language}
        response = self._client.get(f"/movie/{movie_id}/recommendations", params=params)
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
