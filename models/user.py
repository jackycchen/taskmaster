from typing import Optional
import duckdb
from pydantic import BaseModel
from fastapi import HTTPException
import bcrypt
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[int] = None
    username: str
    password_hash: str
    email: Optional[str] = None
    avatar: Optional[str] = None
    created_at: Optional[str] = None

class User:
    @staticmethod
    def init_db():
        conn = duckdb.connect('database.db')
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT,
                    avatar TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        except Exception as e:
            raise Exception(f"Database initialization failed: {str(e)}")
        finally:
            conn.close()

    @staticmethod
    def create(username: str, password: str, email: Optional[str] = None) -> UserModel:
        conn = duckdb.connect('database.db')
        try:
            # 获取当前最大ID
            max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM users").fetchone()[0]
            user_id = max_id + 1
            
            # 使用bcrypt直接加密密码
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            conn.execute(
                "INSERT INTO users (id, username, password_hash, email) VALUES (?, ?, ?, ?)",
                [user_id, username, password_hash, email]
            )
            conn.commit()
            return UserModel(
                id=user_id,
                username=username,
                password_hash=password_hash,
                email=email
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username: str) -> Optional[UserModel]:
        conn = duckdb.connect('database.db')
        try:
            result = conn.execute(
                "SELECT id, username, password_hash, email FROM users WHERE username = ?",
                [username]
            ).fetchone()
            if result:
                return UserModel(
                    id=result[0],
                    username=result[1],
                    password_hash=result[2],
                    email=result[3]
                )
            return None
        finally:
            conn.close()
            
    @staticmethod
    def get_by_id(user_id: int) -> Optional[UserModel]:
        conn = duckdb.connect('database.db')
        try:
            result = conn.execute(
                "SELECT id, username, password_hash, email FROM users WHERE id = ?",
                [user_id]
            ).fetchone()
            if result:
                return UserModel(
                    id=result[0],
                    username=result[1],
                    password_hash=result[2],
                    email=result[3]
                )
            return None
        finally:
            conn.close()