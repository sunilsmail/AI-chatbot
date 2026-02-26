# Order Service

Provides order retrieval and order update operations.

## Runs on
- Port `8002`

## Depends on
- Postgres
- Redis (publishes events to `order_events`)

## Environment
- `DATABASE_URL`
- `REDIS_URL`

## Run independently

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

From `services/order-service`:

```bash
DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce \
REDIS_URL=redis://localhost:6379/0 \
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

## Key endpoints
- `GET /orders/{order_id}`
- `POST /orders/{order_id}/cancel`
- `POST /orders/{order_id}/update-delivery`
- `GET /orders/user/{user_id}`
