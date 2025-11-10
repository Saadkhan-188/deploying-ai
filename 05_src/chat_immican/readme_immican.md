immican-chat/
├─ app/
│  ├─ main.py                # FastAPI entry
│  ├─ api_routes.py          # routes for weather API service, semantic, function
│  ├─ services/
│  │  ├─ api_service.py      # weather/simple external API wrappers + rewriter
│  │  ├─ semantic_service.py # Chroma client, embedding wrappers, hybrid psql metadata sync
│  │  ├─ function_service.py # execute structured actions (calendar, CRUD)
│  │  └─ memory_manager.py   # short-term memory + summarization hook
│  ├─ langgraph_flow.py      # LangGraph flow/agent instantiation & runner
│  ├─ models/                # pydantic models for requests/responses
│  └─ config.py
├─ embeddings_create.py
├─ docker-compose_immican.yml
├─ Dockerfile_immican
├─ requirements.txt
├─ chroma_persist/           # volume mount (in .gitignore)
├─ postgres-init/            # optional SQL init scripts
└─ README_immican.md

## Architecture (short)

FastAPI: main backend exposing /chat and service endpoints. Handles session state, memory management, and executes function actions.

LangGraph: used to orchestrate agent flows (e.g., when chat triggers a chain: retrieve semantically, optionally call web search/LLM, then function call). LangGraph runs inside the container and can be called from FastAPI or embedded via Python API.

ChromaDB: vector store for semantic retrieval (persisted to disk). Use sentence-transformers locally for embeddings (fast, no API keys), or OpenAI embeddings if you prefer.

Postgres (optional hybrid): store structured metadata, user sessions, and message history (recommended for production). For the assignment, you can use in-memory sessions but store documents/metadata in Postgres and vectors in Chroma.

Docker: containerize services; docker-compose for local dev (FastAPI app + Chroma persistence volume + Postgres).

Gradio or React: present a chat UI that calls the FastAPI /chat endpoint. For now you asked for FastAPI — that’s the focus.

## Key design decisions & rationale

Chroma for vectors, Postgres for metadata: Keeps vector ops fast and persisted, while allowing relational joins/filters (e.g., eligibility fields). Chroma stores only vectors + document text + metadata keys; authoritative metadata in Postgres.

Sentence-transformers for embeddings (local): No key, reproducible, quick for a classroom project. Use all-MiniLM-L6-v2.

LangGraph: orchestrates multi-step flows — e.g., semantic search → LLM rewrite → function call. Keep flows simple for this project: build 2-3 flows (QA, API-Transform, Schedule).

Memory management: Keep last N messages; compress older ones into a summary using the LLM (or deterministic summarizer). Store compressed summaries in Postgres as conversation_summaries for later lookups.

Function calling pattern: Assistant returns structured JSON action; backend validates -> executes -> returns confirmation. Always validate times, sanitize inputs.

Testing: Unit test services, integration tests for FastAPI endpoints, and a simple end-to-end test using httpx or pytest-asyncio.


## Commands to run locally (quick)
### build + run (local dev)
docker compose up --build

### optional: run embeddings locally (if not precomputed)
docker exec -it immican-chat_web_1 bash
python embeddings_create.py
.

## Testing

Unit test semantic_service.query, api_service.fetch/rewrite, function_service.execute.

Integration test: start app then use httpx to call /chat with sample messages:

"weather 43.65 -79.38"

"how to apply for a study permit"

"schedule visa consult at 2025-11-10T14:00 for 30m"


## Pitfalls you'll hit (and how to avoid)

Chroma race on first ingest: ensure only one process writes to Chroma on initial ingest. Use a lock or run an initialization job.

Embedding model download during container build: either precompute embeddings or run embedding generation at runtime with a startup script. Building in image can inflate image size.

LangGraph SDK differences: LangGraph API evolves — treat langgraph_flow.py as pattern code; adapt to your SDK.

Timezones: normalize schedule times (ISO8601 with timezone), store in UTC in DB.

Session explosion: use Redis for session state in production; do not rely on in-memory dict.