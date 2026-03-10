# What to Watch — Agent Instructions

See [PROJECT.md](PROJECT.md) for product vision and [ARCHITECTURE.md](ARCHITECTURE.md) for technical decisions and stack.

## Project Structure

```
what-to-watch/
├── main.py                        # FastAPI app entrypoint
├── frontend.py                    # Streamlit chat UI
├── app/
│   ├── config.py                  # Settings (pydantic-settings, reads .env)
│   ├── routers/
│   │   └── recommendations.py     # POST /chat endpoint
│   └── services/
│       ├── llm_service.py         # LangGraph agent + tools
│       ├── tmdb_service.py        # TMDB API client
│       └── external_api_service.py
└── .env                           # API keys (not committed)
```

## Key Files

1. [app/services/llm_service.py](app/services/llm_service.py) — Agent definition and tools
2. [app/routers/recommendations.py](app/routers/recommendations.py) — API endpoint
3. [app/config.py](app/config.py) — Configuration and secrets
4. [app/services/tmdb_service.py](app/services/tmdb_service.py) — TMDB integration

## Development Conventions

- Language: Spanish for UI/user-facing text, English for code
- Keep LLM calls minimal to optimize costs — prefer caching and tool reuse
- The agent should recommend 3-5 movies with a brief explanation and a "Watch Now" link
- TMDB is the primary data source for movie metadata

## Git Workflow

- After completing each task, always create a git commit automatically without waiting to be asked
- Commit message format: `feat: <task subject in lowercase English>`
- Stage only the files modified by that task (never `git add -A`)
