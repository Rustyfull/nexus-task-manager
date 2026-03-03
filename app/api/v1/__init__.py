from fastapi import  APIRouter
from app.api.v1 import auth, users, tasks, projects, health

api_v1_router = APIRouter(prefix="/api/v1")

# Include all routers
api_v1_router.include_router(users.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(tasks.router)
api_v1_router.include_router(projects.router)
api_v1_router.include_router(tasks.router)

