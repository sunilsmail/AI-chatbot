from fastapi import FastAPI
from app.routers import router
from app.core.logging import configure_logging
from app.middleware import add_middleware

def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="order-service")
    add_middleware(app)
    app.include_router(router)
    return app

app = create_app()
