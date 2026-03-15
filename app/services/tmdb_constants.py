"""
Static lookup tables and resolvers for TMDB API values.

These lists are stable and cached here to avoid unnecessary API calls.
Sources:
  - Genres:     https://api.themoviedb.org/3/genre/movie/list
  - Countries:  https://api.themoviedb.org/3/configuration/countries
  - Providers:  https://api.themoviedb.org/3/watch/providers/movie
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Genres — name (EN/ES) → TMDB genre ID
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
    "familia": 10751,
    "fantasía": 14,
    "fantasia": 14,
    "historia": 36,
    "terror": 27,
    "música": 10402,
    "musica": 10402,
    "misterio": 9648,
    "ciencia ficción": 878,
    "ciencia ficcion": 878,
    "bélico": 10752,
    "belico": 10752,
    "guerra": 10752,
    "oeste": 37,
}

# ---------------------------------------------------------------------------
# Countries — name (english / native) → ISO 3166-1 alpha-2 code
# Top 20 by film production volume
# ---------------------------------------------------------------------------
COUNTRY_MAP: dict[str, str] = {
    "united states of america": "US",
    "united states": "US",
    "india": "IN",
    "united kingdom": "GB",
    "france": "FR",
    "japan": "JP",
    "china": "CN",
    "germany": "DE",
    "south korea": "KR",
    "italy": "IT",
    "spain": "ES",
    "canada": "CA",
    "australia": "AU",
    "mexico": "MX",
    "brazil": "BR",
    "russia": "RU",
    "hong kong": "HK",
    "hong kong sar china": "HK",
    "sweden": "SE",
    "denmark": "DK",
    "argentina": "AR",
    "iran": "IR",
}

# ---------------------------------------------------------------------------
# Languages — name (EN/ES) → ISO 639-1 code
# Top languages by film production volume
# ---------------------------------------------------------------------------
LANGUAGE_MAP: dict[str, str] = {
    # English names
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "japanese": "ja",
    "korean": "ko",
    "chinese": "zh",
    "mandarin": "zh",
    "cantonese": "cn",
    "hindi": "hi",
    "arabic": "ar",
    "russian": "ru",
    "turkish": "tr",
    "thai": "th",
    "swedish": "sv",
    "danish": "da",
    "norwegian": "no",
    "finnish": "fi",
    "dutch": "nl",
    "polish": "pl",
    "czech": "cs",
    "romanian": "ro",
    "greek": "el",
    "hebrew": "he",
    "persian": "fa",
    "indonesian": "id",
    "malay": "ms",
    "vietnamese": "vi",
    "tagalog": "tl",
    "tamil": "ta",
    "telugu": "te",
    "bengali": "bn",
    # Spanish names
    "inglés": "en",
    "ingles": "en",
    "español": "es",
    "espanol": "es",
    "francés": "fr",
    "frances": "fr",
    "alemán": "de",
    "aleman": "de",
    "italiano": "it",
    "portugués": "pt",
    "portugues": "pt",
    "japonés": "ja",
    "japones": "ja",
    "coreano": "ko",
    "chino": "zh",
    "mandarín": "zh",
    "mandarin": "zh",
    "cantonés": "cn",
    "cantones": "cn",
    "árabe": "ar",
    "arabe": "ar",
    "ruso": "ru",
    "turco": "tr",
    "tailandés": "th",
    "tailandes": "th",
    "sueco": "sv",
    "danés": "da",
    "danes": "da",
    "noruego": "no",
    "finlandés": "fi",
    "finlandes": "fi",
    "holandés": "nl",
    "holandes": "nl",
    "neerlandés": "nl",
    "neerlandes": "nl",
    "polaco": "pl",
    "checo": "cs",
    "rumano": "ro",
    "griego": "el",
    "hebreo": "he",
    "persa": "fa",
    "indonesio": "id",
    "malayo": "ms",
    "vietnamita": "vi",
    "tagalo": "tl",
}

# ---------------------------------------------------------------------------
# Valid sort_by values for /discover/movie
# ---------------------------------------------------------------------------
VALID_SORT_BY: set[str] = {
    "popularity.desc",
    "popularity.asc",
    "vote_average.desc",
    "vote_average.asc",
    "primary_release_date.desc",
    "primary_release_date.asc",
    "revenue.desc",
    "revenue.asc",
}

# ---------------------------------------------------------------------------
# Streaming providers — name (EN/ES) → TMDB provider ID
# ---------------------------------------------------------------------------
PROVIDER_MAP: dict[str, int] = {
    # Major global platforms
    "netflix": 8,
    "disney plus": 337,
    "disney+": 337,
    "apple tv": 350,
    "apple tv+": 350,
    "amazon prime video": 119,
    "prime video": 119,
    "amazon prime": 119,
    "apple tv store": 2,
    "hbo max": 1899,
    "max": 1899,
    "mubi": 11,
    "amazon video": 10,
    "google play movies": 3,
    "youtube premium": 188,
    "rakuten tv": 35,
    "pluto tv": 300,
    "plex": 538,
    "curiosity stream": 190,
    "docsville": 475,
    "guidedoc": 100,
    "wow presents plus": 546,
    "magellan tv": 551,
    "broadwayhd": 554,
    "filmzie": 559,
    "dekkoo": 444,
    "true story": 567,
    "docalliance films": 569,
    "hoichoi": 315,
    "eventive": 677,
    "cultpix": 692,
    "mubi amazon channel": 201,
    "outtv amazon channel": 607,
    "flixolé amazon channel": 684,
    "flixole amazon channel": 684,
    "tvcortos amazon channel": 689,
    # Spanish-specific
    "movistar plus+": 2241,
    "movistar plus": 2241,
    "movistar plus+ ficción total": 149,
    "movistar plus ficcion total": 149,
    "filmin": 63,
    "filmin plus": 64,
    "atres player": 62,
    "flixolé": 393,
    "flixole": 393,
    "rtve": 541,
    "skyshowtime": 1773,
    "fubotv": 257,
    # Spanish aliases
    "prime": 119,
}

VALID_MONETIZATION_TYPES: set[str] = {"flatrate", "free", "ads", "rent", "buy"}


# ---------------------------------------------------------------------------
# Resolvers — convert human-readable names to TMDB IDs/codes
# ---------------------------------------------------------------------------


def resolve_genre_id(genre: str) -> int | None:
    """Return the TMDB genre ID for a genre name, or None if unknown."""
    return GENRE_MAP.get(genre.lower().strip())


def resolve_provider_id(provider: str) -> int | None:
    """Return the TMDB provider ID for a provider name, or None if unknown."""
    return PROVIDER_MAP.get(provider.lower().strip())


def resolve_language_code(language: str) -> str | None:
    """Return the ISO 639-1 code for a language name, or None if unknown.

    Accepts both language names ('korean') and raw ISO codes ('ko').
    """
    normalized = language.lower().strip()
    if len(normalized) == 2 and normalized.isalpha():
        return normalized
    return LANGUAGE_MAP.get(normalized)


def resolve_country_code(country: str) -> str | None:
    """Return the ISO 3166-1 code for a country name, or None if unknown.

    Accepts both country names ('spain') and raw ISO codes ('ES').
    """
    normalized = country.strip()
    if len(normalized) == 2 and normalized.isalpha():
        return normalized.upper()
    return COUNTRY_MAP.get(normalized.lower())


def resolve_genres(names: list[str]) -> tuple[str | None, str | None]:
    """Resolve a list of genre names to a pipe-separated string of TMDB IDs.

    Returns (ids_string, None) on success, or (None, error_message) on failure.
    """
    ids = []
    unknown = []
    for name in names:
        gid = resolve_genre_id(name)
        if gid is None:
            unknown.append(name)
        else:
            ids.append(str(gid))
    if unknown:
        return None, f"Género(s) no reconocido(s): {', '.join(unknown)}."
    return "|".join(ids), None


def resolve_providers(names: list[str]) -> tuple[str | None, str | None]:
    """Resolve a list of provider names to a pipe-separated string of TMDB IDs.

    Returns (ids_string, None) on success, or (None, error_message) on failure.
    """
    ids = []
    unknown = []
    for name in names:
        pid = resolve_provider_id(name)
        if pid is None:
            unknown.append(name)
        else:
            ids.append(str(pid))
    if unknown:
        return None, f"Plataforma(s) no reconocida(s): {', '.join(unknown)}. Busca sin filtro de plataforma."
    return "|".join(ids), None
