from fastapi import APIRouter
from api import auth, tasks, reminders

# 创建主路由
api_router = APIRouter()

# 包含所有路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])

# 导出主路由
__all__ = ["api_router"]