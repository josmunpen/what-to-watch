# What to Watch

A personal project to practice agentic architectures and MCP (Model Context Protocol).

A web app where users chat with an AI bot that recommends movies based on their tastes and current mood — no more endless scrolling on Netflix.

## What It Does

1. The user chats with the bot describing what they feel like watching (e.g. "Something like Interstellar but less dense")
2. The agent uses an LLM + TMDB to find matching movies in real time
3. The user gets 3-5 personalized recommendations, each with a brief explanation and a "Watch Now" button

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Agent framework:** LangGraph (ReAct loop)
- **LLM:** OpenAI GPT-4
- **Movie data:** TMDB API
- **Observability:** LangSmith

## Setup

### Prerequisites

- Python 3.9+
- API keys: OpenAI, TMDB, LangSmith

### Install

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows PowerShell
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=...
DEFAULT_MODEL=gpt-4o
TMDB_API_KEY=...
TMDB_BASE_URL=https://api.themoviedb.org/3
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=what-to-watch
```

### Run

```bash
# Terminal 1 — Backend
uvicorn main:app --reload

# Terminal 2 — Frontend
streamlit run frontend.py
```

- Frontend: http://localhost:8501
- API: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

## Roadmap

- **v1 (current):** Streamlit + FastAPI + LangGraph agent + TMDB
- **v2:** NoSQL user profiles, FAISS vector DB for semantic search, MCP integration, conversation memory

## Contributing / Agent Context

See [CLAUDE.md](CLAUDE.md) for detailed instructions on project structure, conventions, and architecture — useful both for human contributors and AI coding agents.
