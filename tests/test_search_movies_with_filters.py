from unittest.mock import MagicMock, patch

import pytest

from app.models.movie import Movie


def _make_movie(**overrides) -> Movie:
    defaults = {
        "id": 1,
        "title": "Test Movie",
        "overview": "A test movie.",
        "release_date": "2024-01-01",
        "vote_average": 7.5,
        "genre_ids": [28],
    }
    defaults.update(overrides)
    return Movie(**defaults)


@pytest.fixture
def llm_service():
    """Create an LLMService with a mocked TMDBService (no real HTTP or OpenAI calls)."""
    mock_tmdb = MagicMock()
    mock_tmdb.discover_movies.return_value = [_make_movie()]

    with patch("app.services.llm_service.settings") as mock_settings:
        mock_settings.openai_api_key = "fake-key"
        mock_settings.default_model = "gpt-4"

        from app.services.llm_service import LLMService

        service = LLMService(tmdb=mock_tmdb)

    return service, mock_tmdb


# ---------------------------------------------------------------------------
# sort_by validation
# ---------------------------------------------------------------------------


class TestSortByValidation:
    def test_valid_sort_by(self, llm_service):
        service, mock_tmdb = llm_service
        result = service._search_movies_with_filters(sort_by="vote_average.desc")
        assert "no válido" not in result
        mock_tmdb.discover_movies.assert_called_once()

    def test_invalid_sort_by(self, llm_service):
        service, _ = llm_service
        result = service._search_movies_with_filters(sort_by="invalid.desc")
        assert "sort_by no válido" in result

    def test_default_sort_by(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters()
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["sort_by"] == "popularity.desc"


# ---------------------------------------------------------------------------
# watch_region validation
# ---------------------------------------------------------------------------


class TestWatchRegionValidation:
    def test_valid_iso_code(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(watch_region="US")
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["watch_region"] == "US"

    def test_valid_country_name(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(watch_region="spain")
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["watch_region"] == "ES"

    def test_invalid_region(self, llm_service):
        service, _ = llm_service
        result = service._search_movies_with_filters(watch_region="narnia")
        assert "Región no reconocida" in result

    def test_default_region_es(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters()
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["watch_region"] == "ES"


# ---------------------------------------------------------------------------
# with_original_language validation
# ---------------------------------------------------------------------------


class TestLanguageValidation:
    def test_valid_iso_code(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(with_original_language="ko")
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["with_original_language"] == "ko"

    def test_valid_language_name(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(with_original_language="korean")
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["with_original_language"] == "ko"

    def test_valid_spanish_language_name(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(with_original_language="coreano")
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["with_original_language"] == "ko"

    def test_invalid_language(self, llm_service):
        service, _ = llm_service
        result = service._search_movies_with_filters(with_original_language="klingon")
        assert "Idioma no reconocido" in result

    def test_none_language_not_sent(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters()
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["with_original_language"] is None


# ---------------------------------------------------------------------------
# with_genres validation
# ---------------------------------------------------------------------------


class TestGenresValidation:
    def test_valid_genres(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(with_genres=["horror", "comedy"])
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["with_genres"] == "27|35"

    def test_invalid_genre(self, llm_service):
        service, _ = llm_service
        result = service._search_movies_with_filters(with_genres=["reggaeton"])
        assert "no reconocido" in result

    def test_none_genres(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters()
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["with_genres"] is None


# ---------------------------------------------------------------------------
# without_genres validation
# ---------------------------------------------------------------------------


class TestWithoutGenresValidation:
    def test_valid_excluded_genres(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(without_genres=["comedy"])
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["without_genres"] == "35"

    def test_invalid_excluded_genre(self, llm_service):
        service, _ = llm_service
        result = service._search_movies_with_filters(without_genres=["foo"])
        assert "no reconocido" in result


# ---------------------------------------------------------------------------
# with_watch_providers validation
# ---------------------------------------------------------------------------


class TestProvidersValidation:
    def test_valid_providers(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(with_watch_providers=["netflix", "disney plus"])
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["with_watch_providers"] == "8|337"

    def test_invalid_provider(self, llm_service):
        service, _ = llm_service
        result = service._search_movies_with_filters(with_watch_providers=["blockbuster"])
        assert "no reconocida" in result


# ---------------------------------------------------------------------------
# with_watch_monetization_types validation
# ---------------------------------------------------------------------------


class TestMonetizationValidation:
    def test_valid_monetization(self, llm_service):
        service, mock_tmdb = llm_service
        result = service._search_movies_with_filters(with_watch_monetization_types="flatrate")
        assert "no válido" not in result
        mock_tmdb.discover_movies.assert_called_once()

    def test_invalid_monetization(self, llm_service):
        service, _ = llm_service
        result = service._search_movies_with_filters(with_watch_monetization_types="pirate")
        assert "Tipo de monetización no válido" in result


# ---------------------------------------------------------------------------
# Passthrough params (no validation, just forwarded)
# ---------------------------------------------------------------------------


class TestPassthroughParams:
    def test_numeric_params_forwarded(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(
            primary_release_year=2020,
            vote_average_gte=7.0,
            vote_count_gte=200,
            runtime_gte=90,
            runtime_lte=150,
        )
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["primary_release_year"] == 2020
        assert call_kwargs["vote_average_gte"] == 7.0
        assert call_kwargs["vote_count_gte"] == 200
        assert call_kwargs["runtime_gte"] == 90
        assert call_kwargs["runtime_lte"] == 150

    def test_date_params_forwarded(self, llm_service):
        service, mock_tmdb = llm_service
        service._search_movies_with_filters(
            release_date_gte="2000-01-01",
            release_date_lte="2010-12-31",
        )
        call_kwargs = mock_tmdb.discover_movies.call_args.kwargs
        assert call_kwargs["release_date_gte"] == "2000-01-01"
        assert call_kwargs["release_date_lte"] == "2010-12-31"
