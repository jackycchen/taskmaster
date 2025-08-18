from typing import Optional
import duckdb
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime

class TaskModel(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = 2  # 1=高, 2=中, 3=低
    status: str = "pending"  # pending, in_progress, completed
    created_at: Optional[datetime] = None
    notified: bool = False

class Task:
    @staticmethod
    def init_db():
        conn = duckdb.connect('database.db')
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TIMESTAMP,
                    priority INTEGER DEFAULT 2,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notified BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            conn.commit()
        except Exception as e:
            raise Exception(f"Task table initialization failed: {str(e)}")
        finally:
            conn.close()

    @staticmethod
    def create(user_id: int, title: str, description: str = None, due_date: datetime = None, 
               priority: int = 2, status: str = "pending") -> TaskModel:
        conn = duckdb.connect('database.db')
        try:
            # 获取当前最大ID
            max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM tasks").fetchone()[0]
            task_id = max_id + 1
            
            conn.execute(
                """INSERT INTO tasks (id, user_id, title, description, due_date, priority, status) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [task_id, user_id, title, description, due_date, priority, status]
            )
            conn.commit()
            
            return TaskModel(
                id=task_id,
                user_id=user_id,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id: int) -> list:
        conn = duckdb.connect('database.db')
        try:
            results = conn.execute(
                """SELECT id, user_id, title, description, due_date, priority, status, created_at, notified 
                   FROM tasks WHERE user_id = ? ORDER BY created_at DESC""",
                [user_id]
            ).fetchall()
            
            tasks = []
            for result in results:
                tasks.append(TaskModel(
                    id=result[0],
                    user_id=result[1],
                    title=result[2],
                    description=result[3],
                    due_date=result[4],
                    priority=result[5],
                    status=result[6],
                    created_at=result[7],
                    notified=result[8]
                ))
            return tasks
        finally:
            conn.close()

    @staticmethod
    def get_by_id(task_id: int, user_id: int) -> Optional[TaskModel]:
        conn = duckdb.connect('database.db')
        try:
            result = conn.execute(
                """SELECT id, user_id, title, description, due_date, priority, status, created_at, notified 
                   FROM tasks WHERE id = ? AND user_id = ?""",
                [task_id, user_id]
            ).fetchone()
            
            if result:
                return TaskModel(
                    id=result[0],
                    user_id=result[1],
                    title=result[2],
                    description=result[3],
                    due_date=result[4],
                    priority=result[5],
                    status=result[6],
                    created_at=result[7],
                    notified=result[8]
                )
            return None
        finally:
            conn.close()

    @staticmethod
    def update(task_id: int, user_id: int, title: str = None, description: str = None, 
               due_date: datetime = None, priority: int = None, status: str = None) -> Optional[TaskModel]:
        conn = duckdb.connect('database.db')
        try:
            # 构建动态更新语句
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = ?")
                params.append(title)
                
            if description is not None:
                updates.append("description = ?")
                params.append(description)
                
            if due_date is not None:
                updates.append("due_date = ?")
                params.append(due_date)
                
            if priority is not None:
                updates.append("priority = ?")
                params.append(priority)
                
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            if not updates:
                return None
                
            params.extend([task_id, user_id])
            update_sql = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
            
            conn.execute(update_sql, params)
            conn.commit()
            
            # 返回更新后的任务
            return Task.get_by_id(task_id, user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            conn.close()

    @staticmethod
    def delete(task_id: int, user_id: int) -> bool:
        conn = duckdb.connect('database.db')
        try:
            conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", [task_id, user_id])
            conn.commit()
            return conn.cursor().rowcount > 0
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            conn.close()

    @staticmethod
    def get_due_tasks(minutes_before: int = 30) -> list:
        """获取即将到期的任务"""
        conn = duckdb.connect('database.db')
        try:
            # 查询状态为pending或in_progress，且在指定分钟内到期的任务
            # 使用DuckDB兼容的时间函数
            query = f"""SELECT id, user_id, title, description, due_date, priority, status, created_at, notified 
                       FROM tasks 
                       WHERE status IN ('pending', 'in_progress') 
                       AND notified = FALSE 
                       AND due_date <= NOW() + INTERVAL '{minutes_before}' MINUTE
                       AND due_date >= NOW()"""
            
            results = conn.execute(query).fetchall()
            
            tasks = []
            for result in results:
                tasks.append(TaskModel(
                    id=result[0],
                    user_id=result[1],
                    title=result[2],
                    description=result[3],
                    due_date=result[4],
                    priority=result[5],
                    status=result[6],
                    created_at=result[7],
                    notified=result[8]
                ))
            return tasks
        finally:
            conn.close()

    @staticmethod
    def mark_notified(task_id: int) -> bool:
        """标记任务已提醒"""
        conn = duckdb.connect('database.db')
        try:
            conn.execute("UPDATE tasks SET notified = TRUE WHERE id = ?", [task_id])
            conn.commit()
            return conn.cursor().rowcount > 0
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            conn.close()