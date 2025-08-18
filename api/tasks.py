from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from models.task import Task, TaskModel
from api.auth import get_current_user
from models.user import UserModel

router = APIRouter()

# 数据模型
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = 2  # 1=高, 2=中, 3=低
    status: Optional[str] = "pending"  # pending, in_progress, completed

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: int
    status: str
    created_at: Optional[datetime] = None
    notified: bool

# 创建任务
@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: UserModel = Depends(get_current_user)):
    try:
        new_task = Task.create(
            user_id=current_user.id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            priority=task.priority,
            status=task.status
        )
        return new_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 获取当前用户的所有任务
@router.get("/", response_model=List[TaskResponse])
async def get_tasks(current_user: UserModel = Depends(get_current_user)):
    try:
        tasks = Task.get_by_user_id(current_user.id)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 获取特定任务
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, current_user: UserModel = Depends(get_current_user)):
    try:
        task = Task.get_by_id(task_id, current_user.id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 更新任务
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, current_user: UserModel = Depends(get_current_user)):
    try:
        # 首先检查任务是否存在且属于当前用户
        existing_task = Task.get_by_id(task_id, current_user.id)
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        updated_task = Task.update(
            task_id=task_id,
            user_id=current_user.id,
            title=task_update.title,
            description=task_update.description,
            due_date=task_update.due_date,
            priority=task_update.priority,
            status=task_update.status
        )
        
        if not updated_task:
            raise HTTPException(status_code=400, detail="Failed to update task")
        
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 删除任务
@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: UserModel = Depends(get_current_user)):
    try:
        # 检查任务是否存在且属于当前用户
        existing_task = Task.get_by_id(task_id, current_user.id)
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        result = Task.delete(task_id, current_user.id)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to delete task")
        
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))