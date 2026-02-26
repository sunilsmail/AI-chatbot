# Chat Service

LangGraph-powered chatbot service with chat history storage.

## Runs on
- Port `8004`

## Depends on
- Postgres
- Redis
- order-service (`8002`)
- policy-service (`8003`)
- OpenAI API key for LLM-backed responses

## Environment
- `DATABASE_URL`
- `REDIS_URL`
- `OPENAI_API_KEY`

## Run independently

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-ai.txt
```

From `services/chat-service`:

```bash
DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce \
REDIS_URL=redis://localhost:6379/0 \
OPENAI_API_KEY=your-openai-key \
uvicorn app.main:app --host 0.0.0.0 --port 8004
```

## Key endpoints
- `POST /chat/message`
- `GET /chat/history/{session_id}`
- `GET /metrics`
