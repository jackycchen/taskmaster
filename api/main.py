from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router
from models.user import User
from models.task import Task
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="AceFlow任务管理系统",
    description="多用户隔离的个人任务管理系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix="/api")

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    logger.info("正在初始化数据库...")
    try:
        from models.user import User
        from models.task import Task
        User.init_db()
        Task.init_db()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "系统运行正常"}

# 根路径
@app.get("/")
async def root():
    return {"message": "欢迎使用AceFlow任务管理系统"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)