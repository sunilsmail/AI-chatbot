# AI eCommerce Chatbot Platform

Production-ready microservices platform for AI-assisted eCommerce support.

## Architecture

This repository contains:
- `api-gateway` (request proxy to backend services)
- `auth-service` (registration + login)
- `order-service` (order retrieval, cancellation, delivery updates)
- `policy-service` (product policy lookup)
- `chat-service` (LangGraph multi-agent chat)
- `notification-service` (Redis Pub/Sub consumer)
- `frontend` (React + Vite UI)

## Prerequisites

- Docker + Docker Compose (recommended for full stack)
- OR Python 3.11 + Node 20 if running services independently

## Environment variables

All backend services use values compatible with `.env.example`:

```env
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=ecommerce
DATABASE_URL=postgresql+asyncpg://app:app@postgres:5432/ecommerce
REDIS_URL=redis://redis:6379/0
JWT_SECRET=super-secret
JWT_ALGORITHM=HS256
OPENAI_API_KEY=change-me
```

When running services independently (outside Docker Compose), update hostnames in env values:
- Use `localhost` instead of Docker service names (`postgres`, `redis`, etc.)
- For `api-gateway`, point service URLs to locally running service ports

---

## Docker run flow

### Full stack (single command)

```bash
docker compose up --build
```

### Service-by-service with Docker

Start dependencies first:

```bash
docker compose up -d postgres redis
```

Start backend services one by one:

```bash
docker compose up -d auth-service
docker compose up -d order-service
docker compose up -d policy-service
docker compose up -d chat-service
docker compose up -d notification-service
docker compose up -d api-gateway
```

Start frontend:

```bash
docker compose up -d frontend
```

Service ports:
- Frontend: `http://localhost:5173`
- API Gateway: `http://localhost:8000`
- Auth: `http://localhost:8001`
- Orders: `http://localhost:8002`
- Policies: `http://localhost:8003`
- Chat: `http://localhost:8004`
- Notifications: `http://localhost:8005`
- Postgres: `localhost:5432`
- Redis: `localhost:6379`

---

## Non-Docker local run flow (service-by-service)

> Each subproject has its own README with Docker and non-Docker instructions.

- `frontend/README.md`
- `services/api-gateway/README.md`
- `services/auth-service/README.md`
- `services/order-service/README.md`
- `services/policy-service/README.md`
- `services/chat-service/README.md`
- `services/notification-service/README.md`

### 1) Start shared dependencies without Docker

Install and start Postgres + Redis locally using your OS package manager/service manager.

Create the database once:

```bash
createdb -h localhost -p 5432 -U app ecommerce
```

### 2) Install backend dependencies once

From repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-ai.txt
```

### 3) Run backend services in separate terminals

```bash
# terminal 1
cd services/auth-service && DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce REDIS_URL=redis://localhost:6379/0 uvicorn app.main:app --host 0.0.0.0 --port 8001

# terminal 2
cd services/order-service && DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce REDIS_URL=redis://localhost:6379/0 uvicorn app.main:app --host 0.0.0.0 --port 8002

# terminal 3
cd services/policy-service && DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce uvicorn app.main:app --host 0.0.0.0 --port 8003

# terminal 4
cd services/chat-service && DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce REDIS_URL=redis://localhost:6379/0 OPENAI_API_KEY=your-key uvicorn app.main:app --host 0.0.0.0 --port 8004

# terminal 5
cd services/notification-service && REDIS_URL=redis://localhost:6379/0 uvicorn app.main:app --host 0.0.0.0 --port 8005

# terminal 6 (api-gateway)
cd services/api-gateway && AUTH_SERVICE_URL=http://localhost:8001 ORDER_SERVICE_URL=http://localhost:8002 POLICY_SERVICE_URL=http://localhost:8003 CHAT_SERVICE_URL=http://localhost:8004 NOTIFICATION_SERVICE_URL=http://localhost:8005 uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4) Run frontend

```bash
cd frontend
npm install
npm run dev
```

### 5) Smoke-check each service

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
curl http://localhost:8000/health
```

---

## Kubernetes deploy

```bash
kubectl apply -f k8s/
```
