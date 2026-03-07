"""
Static lookup tables for TMDB API values.

These lists are stable and cached here to avoid unnecessary API calls.
Sources:
  - Genres:   https://api.themoviedb.org/3/genre/movie/list
  - Countries: https://api.themoviedb.org/3/configuration/countries
"""

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
