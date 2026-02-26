from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Policy

router = APIRouter(prefix='/policies', tags=['policies'])

@router.get('/product/{product_id}')
async def get_policy(product_id: int, db: AsyncSession = Depends(get_db)):
    policy = await db.get(Policy, product_id)
    if not policy: raise HTTPException(404, 'Policy not found')
    return {
        'product_id': product_id,
        'cancel_window_hours': policy.cancel_window_hours,
        'refund_policy': policy.refund_policy,
    }
