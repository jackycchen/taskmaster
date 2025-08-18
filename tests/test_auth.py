import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.auth import create_access_token, verify_password

client = TestClient(app)

def test_password_hashing():
    # 测试密码哈希验证
    plain_password = "testpassword"
    hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    assert verify_password(plain_password, hashed_password) == True
    assert verify_password("wrongpassword", hashed_password) == False

def test_token_creation():
    # 测试JWT令牌生成
    token = create_access_token({"sub": "testuser"})
    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT格式校验

def test_protected_route():
    # 测试需要认证的路由
    # 先获取有效token
    token = create_access_token({"sub": "testuser"})
    
    # 带token的请求应该成功
    response = client.get(
        "/auth/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # 不带token的请求应该失败
    response = client.get("/auth/protected")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login():
    # 测试登录流程
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
