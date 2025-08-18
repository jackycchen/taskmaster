from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from models.task import Task, TaskModel

router = APIRouter()

class DueTaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str = None
    due_date: datetime = None
    priority: int
    status: str
    created_at: datetime = None

class NotificationResponse(BaseModel):
    task_id: int
    message: str
    notified_at: datetime = None

# 获取即将到期的任务
@router.get("/due", response_model=List[DueTaskResponse])
async def get_due_tasks(minutes_before: int = 30):
    """
    获取即将到期的任务
    :param minutes_before: 到期前多少分钟提醒，默认30分钟
    """
    try:
        tasks = Task.get_due_tasks(minutes_before)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 标记任务已提醒
@router.post("/mark-notified/{task_id}", response_model=NotificationResponse)
async def mark_task_notified(task_id: int):
    """
    标记任务已提醒
    :param task_id: 任务ID
    """
    try:
        result = Task.mark_notified(task_id)
        if result:
            return NotificationResponse(
                task_id=task_id,
                message=f"Task {task_id} marked as notified",
                notified_at=datetime.now()
            )
        else:
            raise HTTPException(status_code=404, detail="Task not found or already notified")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))