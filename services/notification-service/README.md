# Notification Service

Consumes Redis Pub/Sub messages (channel: `order_events`) and exposes health endpoint.

## Runs on
- Port `8005`

## Depends on
- Redis

## Environment
- `REDIS_URL`

## Docker run

From repository root:

```bash
docker compose up -d notification-service
```

## Non-Docker run

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

From `services/notification-service`:

```bash
REDIS_URL=redis://localhost:6379/0 \
uvicorn app.main:app --host 0.0.0.0 --port 8005
```

## Key endpoints
- `GET /notifications/health`
