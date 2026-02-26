from fastapi import APIRouter
router = APIRouter(prefix='/notifications', tags=['notifications'])

@router.get('/health')
async def health():
    return {'status':'ok'}
