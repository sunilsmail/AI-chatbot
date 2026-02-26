import os

from fastapi import APIRouter, Request
import httpx

router = APIRouter()
ROUTES = {
    'auth': os.getenv('AUTH_SERVICE_URL', 'http://auth-service:8001'),
    'orders': os.getenv('ORDER_SERVICE_URL', 'http://order-service:8002'),
    'policies': os.getenv('POLICY_SERVICE_URL', 'http://policy-service:8003'),
    'chat': os.getenv('CHAT_SERVICE_URL', 'http://chat-service:8004'),
    'notifications': os.getenv('NOTIFICATION_SERVICE_URL', 'http://notification-service:8005'),
}

@router.api_route('/{service}/{path:path}', methods=['GET','POST','PUT','PATCH','DELETE'])
async def proxy(service: str, path: str, request: Request):
    base = ROUTES.get(service)
    if not base:
        return {'error': 'unknown service'}
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            request.method,
            f"{base}/{service}/{path}",
            content=await request.body(),
            headers={k:v for k,v in request.headers.items() if k.lower() != 'host'}
        )
    return resp.json() if resp.headers.get('content-type','').startswith('application/json') else {'raw': resp.text}
