# AI eCommerce Chatbot Platform

Production-ready microservices platform for AI-assisted eCommerce support.

## Services
- `api-gateway`
- `auth-service`
- `order-service`
- `policy-service`
- `chat-service` (LangGraph multi-agent)
- `notification-service` (Redis Pub/Sub)
- `frontend` (React + Vite)

## Local Run
```bash
docker compose up --build
```

## Kubernetes Deploy
```bash
kubectl apply -f k8s/
```
