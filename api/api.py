from fastapi import APIRouter

from api.routes import health_check, tasks, users

api_router = APIRouter()
api_router.include_router(
    health_check.router, prefix="/health_check", tags=["health_check"]
)
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
