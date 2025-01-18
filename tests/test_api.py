import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

test_user_data = {
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
}

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/v1/users/", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "id" in data

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    # First create a user
    await client.post("/api/v1/users/", json=test_user_data)
    
    # Then try to login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_users(client: AsyncClient):
    # First create and login a user
    await client.post("/api/v1/users/", json=test_user_data)
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]
    
    # Then try to get users list
    response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 