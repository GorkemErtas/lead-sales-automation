from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.analytics import router as analytics_router
from app.api.routes.health import router as health_router
from app.api.routes.leads import router as leads_router
from app.api.routes.sales import router as sales_router
from app.core.config import settings

STATIC_DIR = Path(__file__).resolve().parent / "static"

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.2.0")
    app.include_router(health_router)
    app.include_router(leads_router)
    app.include_router(sales_router)
    app.include_router(analytics_router)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/dashboard", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(STATIC_DIR / "dashboard.html")

    return app

app = create_app()
