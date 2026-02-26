# Frontend

React + Vite user interface for the AI eCommerce chatbot platform.

## Runs on
- Port `5173`

## Depends on
- API Gateway (`http://localhost:8000`) for backend access

## Docker run

From repository root:

```bash
docker compose up -d frontend
```

## Non-Docker run

From `frontend`:

```bash
npm install
npm run dev
```

Build for production:

```bash
npm run build
```
