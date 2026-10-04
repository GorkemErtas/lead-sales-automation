from fastapi import FastAPI

from app.api.routes.analytics import router as analytics_router
from app.api.routes.health import router as health_router
from app.api.routes.leads import router as leads_router
from app.api.routes.sales import router as sales_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(health_router)
    app.include_router(leads_router)
    app.include_router(sales_router)
    app.include_router(analytics_router)
    return app


app = create_app()
