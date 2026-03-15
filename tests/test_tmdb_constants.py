import pytest

from app.services.tmdb_constants import (
    resolve_country_code,
    resolve_genre_id,
    resolve_genres,
    resolve_language_code,
    resolve_provider_id,
    resolve_providers,
)


# ---------------------------------------------------------------------------
# resolve_genre_id
# ---------------------------------------------------------------------------


class TestResolveGenreId:
    def test_english_name(self):
        assert resolve_genre_id("horror") == 27

    def test_spanish_name(self):
        assert resolve_genre_id("terror") == 27

    def test_case_insensitive(self):
        assert resolve_genre_id("Horror") == 27
        assert resolve_genre_id("COMEDY") == 35

    def test_strips_whitespace(self):
        assert resolve_genre_id("  drama  ") == 18

    def test_unknown_returns_none(self):
        assert resolve_genre_id("reggaeton") is None

    def test_alias_sci_fi(self):
        assert resolve_genre_id("sci-fi") == 878
        assert resolve_genre_id("science fiction") == 878


# ---------------------------------------------------------------------------
# resolve_provider_id
# ---------------------------------------------------------------------------


class TestResolveProviderId:
    def test_known_provider(self):
        assert resolve_provider_id("netflix") == 8

    def test_alias(self):
        assert resolve_provider_id("prime video") == 119
        assert resolve_provider_id("amazon prime video") == 119
        assert resolve_provider_id("prime") == 119

    def test_case_insensitive(self):
        assert resolve_provider_id("Netflix") == 8

    def test_unknown_returns_none(self):
        assert resolve_provider_id("blockbuster") is None


# ---------------------------------------------------------------------------
# resolve_language_code
# ---------------------------------------------------------------------------


class TestResolveLanguageCode:
    def test_english_name(self):
        assert resolve_language_code("korean") == "ko"

    def test_spanish_name(self):
        assert resolve_language_code("coreano") == "ko"

    def test_iso_code_passthrough(self):
        assert resolve_language_code("ko") == "ko"
        assert resolve_language_code("fr") == "fr"

    def test_iso_code_case_insensitive(self):
        assert resolve_language_code("KO") == "ko"

    def test_strips_whitespace(self):
        assert resolve_language_code("  japanese  ") == "ja"

    def test_unknown_returns_none(self):
        assert resolve_language_code("klingon") is None

    def test_three_letter_code_not_passthrough(self):
        assert resolve_language_code("kor") is None


# ---------------------------------------------------------------------------
# resolve_country_code
# ---------------------------------------------------------------------------


class TestResolveCountryCode:
    def test_country_name(self):
        assert resolve_country_code("spain") == "ES"

    def test_iso_code_passthrough(self):
        assert resolve_country_code("ES") == "ES"

    def test_iso_code_lowercase(self):
        assert resolve_country_code("es") == "ES"

    def test_strips_whitespace(self):
        assert resolve_country_code("  japan  ") == "JP"

    def test_unknown_returns_none(self):
        assert resolve_country_code("narnia") is None

    def test_three_letter_code_not_passthrough(self):
        assert resolve_country_code("ESP") is None


# ---------------------------------------------------------------------------
# resolve_genres (batch)
# ---------------------------------------------------------------------------


class TestResolveGenres:
    def test_single_genre(self):
        ids, err = resolve_genres(["horror"])
        assert err is None
        assert ids == "27"

    def test_multiple_genres(self):
        ids, err = resolve_genres(["horror", "comedy"])
        assert err is None
        assert ids == "27|35"

    def test_unknown_genre_returns_error(self):
        ids, err = resolve_genres(["horror", "reggaeton"])
        assert ids is None
        assert "reggaeton" in err

    def test_all_unknown(self):
        ids, err = resolve_genres(["foo", "bar"])
        assert ids is None
        assert "foo" in err
        assert "bar" in err

    def test_mixed_languages(self):
        ids, err = resolve_genres(["terror", "comedy"])
        assert err is None
        assert ids == "27|35"


# ---------------------------------------------------------------------------
# resolve_providers (batch)
# ---------------------------------------------------------------------------


class TestResolveProviders:
    def test_single_provider(self):
        ids, err = resolve_providers(["netflix"])
        assert err is None
        assert ids == "8"

    def test_multiple_providers(self):
        ids, err = resolve_providers(["netflix", "disney plus"])
        assert err is None
        assert ids == "8|337"

    def test_unknown_provider_returns_error(self):
        ids, err = resolve_providers(["netflix", "blockbuster"])
        assert ids is None
        assert "blockbuster" in err

    def test_all_unknown(self):
        ids, err = resolve_providers(["foo", "bar"])
        assert ids is None
        assert "foo" in err
        assert "bar" in err
