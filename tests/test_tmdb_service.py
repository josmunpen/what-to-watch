"""Tests for TMDBService — JSON-to-domain transformation logic."""

from unittest.mock import MagicMock, patch

import pytest

from app.models.movie import Movie


def _mock_response(json_data, status_code=200):
    """Create a mock httpx.Response."""
    resp = MagicMock()
    resp.json.return_value = json_data
    resp.status_code = status_code
    resp.raise_for_status.return_value = None
    return resp


@pytest.fixture
def tmdb():
    """Create a TMDBService with a mocked httpx.Client."""
    with patch("app.services.tmdb_service.settings") as mock_settings:
        mock_settings.tmdb_base_url = "https://api.themoviedb.org/3"
        mock_settings.tmdb_api_key = "fake-token"
        from app.services.tmdb_service import TMDBService

        service = TMDBService()

    service._client = MagicMock()
    return service


# ---------------------------------------------------------------------------
# Movie list endpoints (discover, search, trending, similar, etc.)
# ---------------------------------------------------------------------------


SAMPLE_MOVIE_JSON = {
    "id": 27205,
    "title": "Inception",
    "overview": "A thief steals secrets through dreams.",
    "release_date": "2010-07-16",
    "vote_average": 8.4,
    "genre_ids": [28, 878],
}


class TestMovieListTransformation:
    """All endpoints that return list[Movie] share the same transformation."""

    def test_discover_maps_to_movie_objects(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": [SAMPLE_MOVIE_JSON]})
        movies = tmdb.discover_movies(with_genres="28")
        assert len(movies) == 1
        m = movies[0]
        assert isinstance(m, Movie)
        assert m.id == 27205
        assert m.title == "Inception"
        assert m.vote_average == 8.4
        assert m.genre_ids == [28, 878]

    def test_search_maps_to_movie_objects(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": [SAMPLE_MOVIE_JSON]})
        movies = tmdb.search_movies("Inception")
        assert len(movies) == 1
        assert movies[0].title == "Inception"

    def test_trending_maps_to_movie_objects(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": [SAMPLE_MOVIE_JSON]})
        movies = tmdb.get_trending_movies("week")
        assert len(movies) == 1
        assert movies[0].title == "Inception"

    def test_similar_maps_to_movie_objects(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": [SAMPLE_MOVIE_JSON]})
        movies = tmdb.get_similar_movies(27205)
        assert len(movies) == 1
        assert movies[0].title == "Inception"

    def test_recommendations_maps_to_movie_objects(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": [SAMPLE_MOVIE_JSON]})
        movies = tmdb.get_movie_recommendations(27205)
        assert len(movies) == 1
        assert movies[0].title == "Inception"

    def test_now_playing_maps_to_movie_objects(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": [SAMPLE_MOVIE_JSON]})
        movies = tmdb.get_now_playing_movies()
        assert len(movies) == 1
        assert movies[0].title == "Inception"

    def test_empty_results(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": []})
        assert tmdb.discover_movies() == []

    def test_missing_optional_fields_use_defaults(self, tmdb):
        minimal = {"id": 1, "title": "Minimal"}
        tmdb._client.get.return_value = _mock_response({"results": [minimal]})
        movies = tmdb.discover_movies()
        m = movies[0]
        assert m.overview == ""
        assert m.release_date == ""
        assert m.vote_average == 0.0
        assert m.genre_ids == []


# ---------------------------------------------------------------------------
# get_movie_watch_providers — complex categorization
# ---------------------------------------------------------------------------


class TestWatchProvidersTransformation:
    def test_all_categories(self, tmdb):
        tmdb._client.get.return_value = _mock_response({
            "results": {
                "ES": {
                    "flatrate": [{"provider_name": "Netflix"}, {"provider_name": "HBO Max"}],
                    "rent": [{"provider_name": "Apple TV"}],
                    "buy": [{"provider_name": "Google Play"}],
                    "free": [{"provider_name": "Tubi"}],
                    "ads": [{"provider_name": "Pluto TV"}],
                },
            }
        })
        providers = tmdb.get_movie_watch_providers(1, watch_region="ES")
        assert providers["flatrate"] == ["Netflix", "HBO Max"]
        assert providers["rent"] == ["Apple TV"]
        assert providers["buy"] == ["Google Play"]
        assert providers["free"] == ["Tubi"]
        assert providers["ads"] == ["Pluto TV"]

    def test_region_not_available(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": {"US": {"flatrate": [{"provider_name": "Hulu"}]}}})
        providers = tmdb.get_movie_watch_providers(1, watch_region="ES")
        assert providers == {}

    def test_partial_categories(self, tmdb):
        tmdb._client.get.return_value = _mock_response({
            "results": {"ES": {"flatrate": [{"provider_name": "Netflix"}]}}
        })
        providers = tmdb.get_movie_watch_providers(1, watch_region="ES")
        assert "flatrate" in providers
        assert "rent" not in providers
        assert "buy" not in providers

    def test_empty_results(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": {}})
        providers = tmdb.get_movie_watch_providers(1)
        assert providers == {}


# ---------------------------------------------------------------------------
# search_person — structured person data
# ---------------------------------------------------------------------------


class TestSearchPersonTransformation:
    def test_person_with_known_for(self, tmdb):
        tmdb._client.get.return_value = _mock_response({
            "results": [{
                "id": 6193,
                "name": "Leonardo DiCaprio",
                "known_for_department": "Acting",
                "known_for": [
                    {"title": "Inception", "media_type": "movie"},
                    {"title": "Titanic", "media_type": "movie"},
                    {"name": "Some TV Show", "media_type": "tv"},
                ],
            }]
        })
        results = tmdb.search_person("DiCaprio")
        assert len(results) == 1
        p = results[0]
        assert p["id"] == 6193
        assert p["name"] == "Leonardo DiCaprio"
        assert p["known_for_department"] == "Acting"
        assert "Inception" in p["known_for"]
        assert "Titanic" in p["known_for"]
        assert "Some TV Show" in p["known_for"]

    def test_person_empty_known_for(self, tmdb):
        tmdb._client.get.return_value = _mock_response({
            "results": [{"id": 1, "name": "Unknown", "known_for_department": "", "known_for": []}]
        })
        results = tmdb.search_person("Unknown")
        assert results[0]["known_for"] == []

    def test_no_results(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"results": []})
        assert tmdb.search_person("nonexistent") == []

    def test_known_for_filters_empty_titles(self, tmdb):
        tmdb._client.get.return_value = _mock_response({
            "results": [{
                "id": 1,
                "name": "Actor",
                "known_for_department": "Acting",
                "known_for": [
                    {"media_type": "movie"},  # no title or name
                    {"title": "Real Movie", "media_type": "movie"},
                ],
            }]
        })
        results = tmdb.search_person("Actor")
        assert results[0]["known_for"] == ["Real Movie"]


# ---------------------------------------------------------------------------
# get_person_movie_credits — cast/crew transformation
# ---------------------------------------------------------------------------


class TestPersonMovieCreditsTransformation:
    def test_cast_and_crew(self, tmdb):
        tmdb._client.get.return_value = _mock_response({
            "cast": [
                {"id": 1, "title": "Film A", "overview": "...", "release_date": "2020-01-01", "vote_average": 8.0, "genre_ids": [28]},
            ],
            "crew": [
                {"id": 2, "title": "Film B", "overview": "...", "release_date": "2019-05-01", "vote_average": 7.0, "genre_ids": [18]},
            ],
        })
        credits = tmdb.get_person_movie_credits(6193)
        assert len(credits["cast"]) == 1
        assert len(credits["crew"]) == 1
        assert isinstance(credits["cast"][0], Movie)
        assert credits["cast"][0].title == "Film A"
        assert credits["crew"][0].title == "Film B"

    def test_filters_entries_without_title(self, tmdb):
        tmdb._client.get.return_value = _mock_response({
            "cast": [
                {"id": 1, "title": "Has Title", "overview": "", "release_date": "", "vote_average": 0, "genre_ids": []},
                {"id": 2, "overview": "No title field"},  # missing title
            ],
            "crew": [],
        })
        credits = tmdb.get_person_movie_credits(1)
        assert len(credits["cast"]) == 1
        assert credits["cast"][0].title == "Has Title"

    def test_empty_credits(self, tmdb):
        tmdb._client.get.return_value = _mock_response({"cast": [], "crew": []})
        credits = tmdb.get_person_movie_credits(1)
        assert credits["cast"] == []
        assert credits["crew"] == []


# ---------------------------------------------------------------------------
# get_movie_details — raw dict passthrough
# ---------------------------------------------------------------------------


class TestGetMovieDetailsTransformation:
    def test_returns_raw_json(self, tmdb):
        raw = {"id": 1, "title": "Test", "runtime": 120}
        tmdb._client.get.return_value = _mock_response(raw)
        result = tmdb.get_movie_details(1)
        assert result == raw
