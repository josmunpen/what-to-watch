from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from app.config import settings
from app.services.tmdb_service import Movie, discover_movies_by_genre
from loguru import logger

SYSTEM_PROMPT = """Eres un experto en cine. Tu misión es recomendar exactamente 1 película al usuario.

Cuando el usuario mencione un género, DEBES usar la herramienta `search_movies_by_genre` para buscar
películas populares de ese género en TMDB. Luego elige la que mejor encaje y recomiéndala incluyendo:
- Título y año
- Por qué se la recomiendas en 1-2 frases
Sé breve, directo y entusiasta. Recomienda solo 1 película."""


@tool
def search_movies_by_genre(genre: str) -> str:
    """Busca en TMDB películas populares de un género dado.
    Úsala siempre que el usuario pida una recomendación por género.
    El género debe estar en inglés (e.g. 'horror', 'comedy', 'thriller', 'action').
    """
    logger.debug(f"LLM requested search_movies_by_genre with genre: {genre}")
    try:
        movies = discover_movies_by_genre(genre, page=1)
    except ValueError as e:
        return str(e)

    return format_movies_for_prompt(movies)


def format_movies_for_prompt(movies: list[Movie]) -> str:
    """Devuelve una lista formateada de películas para mostrar en el prompt."""
    lines = []
    for m in movies[:10]:
        year = m.release_date[:4] if m.release_date else "?"
        overview = (
            m.overview[:150] + "..."
            if len(m.overview) > 150
            else m.overview
        )
        lines.append(
            f"- {m.title} ({year}) [score: {m.vote_average:.1f}]: {overview}"
        )
    return "\n".join(lines) if lines else "No movies found for that genre."


llm = ChatOpenAI(model=settings.default_model, api_key=settings.openai_api_key)

# create_agent gestiona el bucle ReAct automáticamente:
# LLM decide llamar a la tool → ToolNode la ejecuta → LLM recibe los resultados y responde.
graph = create_agent(
    llm,
    tools=[search_movies_by_genre],
    system_prompt=SystemMessage(content=SYSTEM_PROMPT),
    # max_iterations=5,
)