# Architecture

See [PROJECT.md](PROJECT.md) for product vision and requirements.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (`frontend.py`) |
| Backend | FastAPI (`main.py`) |
| Agent framework | LangGraph via `create_agent` (ReAct loop) |
| LLM | OpenAI GPT-4 (configured via `settings.default_model`) |
| External API | TMDB (The Movie Database) |
| Observability | LangSmith tracing |
| Config | `pydantic-settings` with `.env` file |

## Agent Architecture (v1)

ReAct loop via LangGraph's `create_agent`:
1. User sends a message via Streamlit → POST `/chat`
2. The LangGraph agent receives the message
3. The LLM decides whether to call the `search_movies_by_genre` tool (TMDB API)
4. The LLM generates a final recommendation response

## Roadmap (v2)

- NoSQL database for user profiles and preferences
- FAISS vector database for semantic movie similarity search
- MCP (Model Context Protocol) integration
- Full conversation memory
