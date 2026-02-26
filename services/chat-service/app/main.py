from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import router
from app.ws import router as ws_router
from app.core.logging import configure_logging
from app.middleware import add_middleware

def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title='chat-service')
    add_middleware(app)
    app.include_router(router)
    app.include_router(ws_router)
    Instrumentator().instrument(app).expose(app)
    return app

app = create_app()
