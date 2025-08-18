from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def main():
    # 创建测试用户
    test_user = User.create(
        username="testuser",
        password="testpass"
    )
    print(f"Created test user: {test_user.username}")

if __name__ == "__main__":
    main()
