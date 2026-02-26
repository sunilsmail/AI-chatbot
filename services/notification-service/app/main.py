import asyncio
from redis.asyncio import Redis
from app.core.settings import settings
from app.routers import router
from app.core.logging import configure_logging
from app.middleware import add_middleware
from fastapi import FastAPI

app=FastAPI(title='notification-service')
configure_logging(); add_middleware(app); app.include_router(router)

@app.on_event('startup')
async def consume():
    async def runner():
        r = Redis.from_url(settings.redis_url)
        pubsub=r.pubsub(); await pubsub.subscribe('order_events')
        async for msg in pubsub.listen():
            if msg.get('type')=='message':
                print('notification event', msg.get('data'))
    asyncio.create_task(runner())
