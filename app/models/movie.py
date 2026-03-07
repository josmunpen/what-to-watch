from dataclasses import dataclass


@dataclass(slots=True)
class Movie:
    """Domain object representing a TMDB movie."""

    id: int
    title: str
    overview: str
    release_date: str
    vote_average: float
    genre_ids: list[int]
