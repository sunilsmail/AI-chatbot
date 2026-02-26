# Policy Service

Serves cancellation/refund policy details by product.

## Runs on
- Port `8003`

## Depends on
- Postgres

## Environment
- `DATABASE_URL`

## Docker run

From repository root:

```bash
docker compose up -d policy-service
```

## Non-Docker run

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

From `services/policy-service`:

```bash
DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce \
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

## Key endpoints
- `GET /policies/product/{product_id}`
