# Auth Service

Handles user registration and login.

## Runs on
- Port `8001`

## Depends on
- Postgres

## Environment
- `DATABASE_URL` (default points to localhost in settings)
- `JWT_SECRET`
- `JWT_ALGORITHM`

## Docker run

From repository root:

```bash
docker compose up -d auth-service
```

## Non-Docker run

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

From `services/auth-service`:

```bash
DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/ecommerce \
JWT_SECRET=super-secret \
JWT_ALGORITHM=HS256 \
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## Key endpoints
- `POST /auth/register`
- `POST /auth/login`
