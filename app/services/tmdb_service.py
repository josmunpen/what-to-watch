"""
TMDB API connector.

Uses the TMDB v3 REST API with a Bearer token (API Read Access Token).
Resolvers and lookup tables live in tmdb_constants.py.
"""

from typing import Any

import httpx

from app.config import settings
from app.models.movie import Movie


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
        with_genres: str | None = None,
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

        All ID-based parameters (with_genres, without_genres, with_watch_providers)
        expect pre-resolved pipe-separated ID strings.

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        params: dict[str, Any] = {
            "sort_by": sort_by,
            "language": language,
            "page": page,
        }
        if with_genres is not None:
            params["with_genres"] = with_genres
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


    def get_movie_watch_providers(
        self,
        movie_id: int,
        watch_region: str = "ES",
    ) -> dict[str, list[str]]:
        """Get watch providers for a movie in a specific region.

        Returns a dict with keys 'flatrate', 'rent', 'buy' (if available),
        each containing a list of provider names.

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        response = self._client.get(f"/movie/{movie_id}/watch/providers")
        response.raise_for_status()

        all_results: dict[str, Any] = response.json().get("results", {})
        region_data = all_results.get(watch_region, {})

        providers: dict[str, list[str]] = {}
        for category in ("flatrate", "rent", "buy", "free", "ads"):
            if category in region_data:
                providers[category] = [
                    p["provider_name"] for p in region_data[category]
                ]
        return providers

    def get_trending_movies(
        self,
        time_window: str = "week",
        language: str = "en-US",
    ) -> list[Movie]:
        """Get trending movies for a given time window.

        Args:
            time_window: "day" or "week".

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        params: dict[str, Any] = {"language": language}
        response = self._client.get(f"/trending/movie/{time_window}", params=params)
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

    def get_movie_details(self, movie_id: int, language: str = "en-US") -> dict[str, Any]:
        """Get full details for a movie.

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        params: dict[str, Any] = {"language": language}
        response = self._client.get(f"/movie/{movie_id}", params=params)
        response.raise_for_status()
        return response.json()

    def get_similar_movies(
        self,
        movie_id: int,
        page: int = 1,
        language: str = "en-US",
    ) -> list[Movie]:
        """Get similar movies based on keywords and genres.

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        params: dict[str, Any] = {"page": page, "language": language}
        response = self._client.get(f"/movie/{movie_id}/similar", params=params)
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

    def get_now_playing_movies(
        self,
        region: str = "ES",
        page: int = 1,
        language: str = "en-US",
    ) -> list[Movie]:
        """Get movies currently in theatres.

        Raises:
            httpx.HTTPStatusError – on non-2xx responses from TMDB.
        """
        params: dict[str, Any] = {"page": page, "language": language, "region": region}
        response = self._client.get("/movie/now_playing", params=params)
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
