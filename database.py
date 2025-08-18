"""
数据库初始化文件
"""
from models.user import User
from models.task import Task

def init_database():
    """
    初始化数据库表
    """
    try:
        User.init_db()
        Task.init_db()
        print("数据库初始化成功")
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        raise e

if __name__ == "__main__":
    init_database()