from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis.asyncio import Redis
from app.db.session import get_db
from app.db.models import Order, OrderStatus
from app.core.settings import settings

router = APIRouter(prefix='/orders', tags=['orders'])

class CancelReq(BaseModel):
    product_id: int

class UpdateDeliveryReq(BaseModel):
    delivery_date: datetime

async def publish(event: str, payload: dict):
    r = Redis.from_url(settings.redis_url)
    await r.publish(event, str(payload))
    await r.aclose()

@router.get('/{order_id}')
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order: raise HTTPException(404, 'Order not found')
    return {'id': order.id, 'status': order.status, 'delivery_date': order.delivery_date}

@router.post('/{order_id}/cancel')
async def cancel_order(order_id: int, _: CancelReq, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order: raise HTTPException(404, 'Order not found')
    if order.status in [OrderStatus.shipped, OrderStatus.delivered]:
        raise HTTPException(400, 'Order cannot be cancelled')
    order.status = OrderStatus.cancelled
    await db.commit(); await publish('order_events', {'type': 'cancelled', 'order_id': order_id})
    return {'message': 'Order item cancellation accepted'}

@router.post('/{order_id}/update-delivery')
async def update_delivery(order_id: int, payload: UpdateDeliveryReq, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order: raise HTTPException(404, 'Order not found')
    order.delivery_date = payload.delivery_date
    await db.commit(); await publish('order_events', {'type':'delivery_updated', 'order_id': order_id})
    return {'message': 'Delivery date updated', 'delivery_date': payload.delivery_date}

@router.get('/user/{user_id}')
async def orders_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    rows = (await db.scalars(select(Order).where(Order.user_id==user_id))).all()
    return [{'id': o.id, 'status': o.status, 'delivery_date': o.delivery_date} for o in rows]
