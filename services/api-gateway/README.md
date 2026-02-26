# API Gateway

Proxies incoming requests to backend services.

## Runs on
- Port `8000`

## Depends on
- auth-service (`8001`)
- order-service (`8002`)
- policy-service (`8003`)
- chat-service (`8004`)
- notification-service (`8005`)

## Run independently

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

From `services/api-gateway`:

```bash
AUTH_SERVICE_URL=http://localhost:8001 \
ORDER_SERVICE_URL=http://localhost:8002 \
POLICY_SERVICE_URL=http://localhost:8003 \
CHAT_SERVICE_URL=http://localhost:8004 \
NOTIFICATION_SERVICE_URL=http://localhost:8005 \
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

These URL overrides are required for non-Docker runs; Docker Compose can keep the default container hostnames.

## Example routes
- `GET /auth/login`
- `POST /orders/123/cancel`
- `GET /policies/product/1`
- `POST /chat/message`
