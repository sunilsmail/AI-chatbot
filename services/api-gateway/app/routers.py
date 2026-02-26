from fastapi import APIRouter, Request
import httpx

router = APIRouter()
ROUTES = {
    'auth': 'http://auth-service:8001',
    'orders': 'http://order-service:8002',
    'policies': 'http://policy-service:8003',
    'chat': 'http://chat-service:8004',
    'notifications': 'http://notification-service:8005',
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
