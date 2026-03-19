"""Tests for _format_movies and tool-level response formatting."""

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
    mock_tmdb = MagicMock()
    with patch("app.services.llm_service.settings") as mock_settings:
        mock_settings.openai_api_key = "fake-key"
        mock_settings.default_model = "gpt-4"
        from app.services.llm_service import LLMService

        service = LLMService(tmdb=mock_tmdb)
    return service, mock_tmdb


# ---------------------------------------------------------------------------
# _format_movies (shared formatter)
# ---------------------------------------------------------------------------


class TestFormatMovies:
    def test_single_movie(self):
        from app.services.llm_service import _format_movies

        movie = _make_movie(title="Inception", release_date="2010-07-16", vote_average=8.4, overview="A mind-bending thriller.")
        result = _format_movies([movie])
        assert result == "- Inception (2010) [score: 8.4]: A mind-bending thriller."

    def test_empty_list(self):
        from app.services.llm_service import _format_movies

        result = _format_movies([])
        assert result == "No movies found for that genre."

    def test_truncates_long_overview(self):
        from app.services.llm_service import _format_movies

        long_overview = "A" * 200
        movie = _make_movie(overview=long_overview)
        result = _format_movies([movie])
        assert result.endswith("...")
        # 150 chars of overview + "..."
        assert "A" * 150 + "..." in result

    def test_missing_release_date(self):
        from app.services.llm_service import _format_movies

        movie = _make_movie(release_date="")
        result = _format_movies([movie])
        assert "(?) " in result

    def test_limits_to_10_movies(self):
        from app.services.llm_service import _format_movies

        movies = [_make_movie(id=i, title=f"Movie {i}") for i in range(15)]
        result = _format_movies(movies)
        lines = result.strip().split("\n")
        assert len(lines) == 10

    def test_multiple_movies_format(self):
        from app.services.llm_service import _format_movies

        movies = [
            _make_movie(title="First", release_date="2020-01-01", vote_average=7.0, overview="Overview one."),
            _make_movie(title="Second", release_date="2021-06-15", vote_average=8.0, overview="Overview two."),
        ]
        result = _format_movies(movies)
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[0].startswith("- First (2020)")
        assert lines[1].startswith("- Second (2021)")

    def test_vote_average_one_decimal(self):
        from app.services.llm_service import _format_movies

        movie = _make_movie(vote_average=7.123)
        result = _format_movies([movie])
        assert "[score: 7.1]" in result


# ---------------------------------------------------------------------------
# _get_movie_details formatting
# ---------------------------------------------------------------------------


class TestGetMovieDetailsFormatting:
    def test_full_details(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_details.return_value = {
            "title": "Inception",
            "release_date": "2010-07-16",
            "tagline": "Your mind is the scene of the crime.",
            "genres": [{"name": "Action"}, {"name": "Sci-Fi"}],
            "runtime": 148,
            "vote_average": 8.4,
            "vote_count": 35000,
            "overview": "A thief who steals secrets through dreams.",
            "budget": 160000000,
            "revenue": 836800000,
            "belongs_to_collection": None,
        }
        result = service._get_movie_details(movie_id=27205)
        assert "**Inception** (2010)" in result
        assert "Action, Sci-Fi" in result
        assert "2h 28min" in result
        assert "8.4/10" in result
        assert "$160,000,000" in result
        assert "$836,800,000" in result

    def test_details_without_budget_revenue(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_details.return_value = {
            "title": "Indie Film",
            "release_date": "2023-03-01",
            "tagline": "",
            "genres": [{"name": "Drama"}],
            "runtime": 90,
            "vote_average": 6.5,
            "vote_count": 100,
            "overview": "A small film.",
            "budget": 0,
            "revenue": 0,
            "belongs_to_collection": None,
        }
        result = service._get_movie_details(movie_id=1)
        assert "Presupuesto" not in result
        assert "Recaudación" not in result

    def test_details_with_collection(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_details.return_value = {
            "title": "The Dark Knight",
            "release_date": "2008-07-18",
            "tagline": "Why so serious?",
            "genres": [{"name": "Action"}],
            "runtime": 152,
            "vote_average": 9.0,
            "vote_count": 30000,
            "overview": "Batman faces the Joker.",
            "budget": 185000000,
            "revenue": 1004558444,
            "belongs_to_collection": {"name": "The Dark Knight Collection"},
        }
        result = service._get_movie_details(movie_id=155)
        assert "Colección: The Dark Knight Collection" in result

    def test_details_none_returns_error(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_details.return_value = None
        result = service._get_movie_details(movie_id=999)
        assert "No se encontraron detalles" in result

    def test_details_zero_runtime(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_details.return_value = {
            "title": "Unknown",
            "release_date": "2020-01-01",
            "tagline": "",
            "genres": [],
            "runtime": 0,
            "vote_average": 0.0,
            "vote_count": 0,
            "overview": "N/A",
            "budget": 0,
            "revenue": 0,
            "belongs_to_collection": None,
        }
        result = service._get_movie_details(movie_id=1)
        assert "0h 0min" in result


# ---------------------------------------------------------------------------
# _get_movie_watch_providers formatting
# ---------------------------------------------------------------------------


class TestGetWatchProvidersFormatting:
    def test_providers_with_all_categories(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_watch_providers.return_value = {
            "flatrate": ["Netflix", "HBO Max"],
            "rent": ["Apple TV"],
            "buy": ["Google Play"],
        }
        result = service._get_movie_watch_providers(movie_id=1)
        assert "Suscripción: Netflix, HBO Max" in result
        assert "Alquiler: Apple TV" in result
        assert "Compra: Google Play" in result

    def test_providers_empty(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_watch_providers.return_value = {}
        result = service._get_movie_watch_providers(movie_id=1)
        assert "No se encontraron plataformas" in result

    def test_providers_free_and_ads(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_watch_providers.return_value = {
            "free": ["Tubi"],
            "ads": ["Pluto TV"],
        }
        result = service._get_movie_watch_providers(movie_id=1)
        assert "Gratis: Tubi" in result
        assert "Con anuncios: Pluto TV" in result

    def test_providers_invalid_region(self, llm_service):
        service, _ = llm_service
        result = service._get_movie_watch_providers(movie_id=1, watch_region="narnia")
        assert "Región no reconocida" in result

    def test_providers_region_resolved(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_watch_providers.return_value = {"flatrate": ["Netflix"]}
        service._get_movie_watch_providers(movie_id=1, watch_region="united states")
        mock_tmdb.get_movie_watch_providers.assert_called_once_with(1, watch_region="US")


# ---------------------------------------------------------------------------
# _search_person formatting
# ---------------------------------------------------------------------------


class TestSearchPersonFormatting:
    def test_person_found(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.search_person.return_value = [
            {"id": 6193, "name": "Leonardo DiCaprio", "known_for_department": "Acting", "known_for": ["Inception", "Titanic", "The Revenant"]},
        ]
        result = service._search_person(query="DiCaprio")
        assert "Leonardo DiCaprio (ID: 6193)" in result
        assert "[Acting]" in result
        assert "Inception, Titanic, The Revenant" in result

    def test_person_not_found(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.search_person.return_value = []
        result = service._search_person(query="xyznotaperson")
        assert "No se encontró ninguna persona" in result

    def test_person_no_known_for(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.search_person.return_value = [
            {"id": 1, "name": "Unknown Actor", "known_for_department": "Acting", "known_for": []},
        ]
        result = service._search_person(query="Unknown")
        assert "N/A" in result

    def test_person_limits_to_5(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.search_person.return_value = [
            {"id": i, "name": f"Person {i}", "known_for_department": "Acting", "known_for": []}
            for i in range(10)
        ]
        result = service._search_person(query="Person")
        lines = result.strip().split("\n")
        assert len(lines) == 5

    def test_person_known_for_limited_to_3(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.search_person.return_value = [
            {"id": 1, "name": "Actor", "known_for_department": "Acting", "known_for": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]},
        ]
        result = service._search_person(query="Actor")
        assert "Alpha, Beta, Gamma" in result
        assert "Delta" not in result


# ---------------------------------------------------------------------------
# _get_person_movie_credits formatting
# ---------------------------------------------------------------------------


class TestGetPersonMovieCreditsFormatting:
    def test_cast_only(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_person_movie_credits.return_value = {
            "cast": [_make_movie(title="Film A", vote_average=8.0), _make_movie(title="Film B", vote_average=6.0)],
            "crew": [],
        }
        result = service._get_person_movie_credits(person_id=1, role="cast")
        assert "**Como actor/actriz:**" in result
        assert "Film A" in result
        assert "equipo técnico" not in result

    def test_crew_only(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_person_movie_credits.return_value = {
            "cast": [],
            "crew": [_make_movie(title="Directed Movie", vote_average=9.0)],
        }
        result = service._get_person_movie_credits(person_id=1, role="crew")
        assert "**Como equipo técnico:**" in result
        assert "Directed Movie" in result
        assert "actor/actriz" not in result

    def test_both_roles(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_person_movie_credits.return_value = {
            "cast": [_make_movie(title="Acted In")],
            "crew": [_make_movie(title="Directed")],
        }
        result = service._get_person_movie_credits(person_id=1, role="both")
        assert "**Como actor/actriz:**" in result
        assert "**Como equipo técnico:**" in result

    def test_cast_sorted_by_vote_desc(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_person_movie_credits.return_value = {
            "cast": [
                _make_movie(title="Low", vote_average=3.0),
                _make_movie(title="High", vote_average=9.0),
                _make_movie(title="Mid", vote_average=6.0),
            ],
            "crew": [],
        }
        result = service._get_person_movie_credits(person_id=1, role="cast")
        high_pos = result.index("High")
        mid_pos = result.index("Mid")
        low_pos = result.index("Low")
        assert high_pos < mid_pos < low_pos

    def test_invalid_role(self, llm_service):
        service, _ = llm_service
        result = service._get_person_movie_credits(person_id=1, role="extra")
        assert "Rol no válido" in result

    def test_empty_credits_cast(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_person_movie_credits.return_value = {
            "cast": [],
            "crew": [],
        }
        result = service._get_person_movie_credits(person_id=1, role="cast")
        assert "Sin créditos" in result


# ---------------------------------------------------------------------------
# Tools that delegate to _format_movies (empty-result messages)
# ---------------------------------------------------------------------------


class TestToolEmptyResults:
    def test_search_by_title_not_found(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.search_movies.return_value = []
        result = service._search_movie_by_title(query="nonexistent")
        assert "No se encontraron películas" in result

    def test_recommendations_not_found(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_movie_recommendations.return_value = []
        result = service._get_movie_recommendations(movie_id=999)
        assert "No se encontraron recomendaciones" in result

    def test_similar_not_found(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_similar_movies.return_value = []
        result = service._get_similar_movies(movie_id=999)
        assert "No se encontraron películas similares" in result

    def test_trending_not_found(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_trending_movies.return_value = []
        result = service._get_trending_movies()
        assert "No se encontraron películas en tendencia" in result

    def test_now_playing_not_found(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_now_playing_movies.return_value = []
        result = service._get_now_playing_movies()
        assert "No se encontraron películas en cartelera" in result


# ---------------------------------------------------------------------------
# _get_trending_movies validation
# ---------------------------------------------------------------------------


class TestTrendingMoviesValidation:
    def test_invalid_time_window(self, llm_service):
        service, _ = llm_service
        result = service._get_trending_movies(time_window="month")
        assert "time_window no válido" in result

    def test_valid_day(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_trending_movies.return_value = [_make_movie()]
        result = service._get_trending_movies(time_window="day")
        assert "no válido" not in result
        mock_tmdb.get_trending_movies.assert_called_once_with("day")


# ---------------------------------------------------------------------------
# _get_now_playing_movies validation
# ---------------------------------------------------------------------------


class TestNowPlayingValidation:
    def test_invalid_region(self, llm_service):
        service, _ = llm_service
        result = service._get_now_playing_movies(region="atlantis")
        assert "Región no reconocida" in result

    def test_region_resolved(self, llm_service):
        service, mock_tmdb = llm_service
        mock_tmdb.get_now_playing_movies.return_value = [_make_movie()]
        service._get_now_playing_movies(region="united states")
        mock_tmdb.get_now_playing_movies.assert_called_once_with(region="US")
