from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import  get_settings
from app.api.v1 import  api_v1_router
from app.models.base import  Base
from app.core.database import engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=get_settings().api_title,
        description=get_settings().api_description,
        version=get_settings().app_version,
        debug=get_settings().debug,
        lifespan=lifespan,
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().cors_origins,
        allow_credentials=get_settings().cors_credentials,
        allow_methods=get_settings().cors_methods,
        allow_headers=get_settings().cors_headers

    )

    # Include routers
    app.include_router(api_v1_router)

    # Root endpoint
    @app.get("/")
    async  def root():
        return {
            "app":get_settings().app_name,
            "version": get_settings().app_version,
            "environment": get_settings().environment,
            "docs":"/api/v1/docs"
        }

    return app



app = create_app()

