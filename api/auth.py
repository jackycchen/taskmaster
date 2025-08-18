import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from models.user import User
from typing import Optional

router = APIRouter()

# 安全配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

import logging
logger = logging.getLogger(__name__)

@router.post("/register")
def register(user: UserCreate):
    try:
        logger.info(f"Register attempt for username: {user.username}")
        
        # 检查用户名是否已存在
        existing_user = User.get_by_username(user.username)
        if existing_user:
            logger.warning(f"Username already exists: {user.username}")
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 创建用户
        new_user = User.create(
            username=user.username,
            password=user.password,
            email=user.email
        )
        
        logger.info(f"User created successfully: {user.username}")
        return {"message": "用户注册成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed for {user.username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="注册过程中发生错误")

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.get_by_username(form_data.username)
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    # 生成JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = User.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "You have access to protected route"}