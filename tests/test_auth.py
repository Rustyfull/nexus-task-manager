import  pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    payload = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "bonjour123@",
            "full_name": "New User"
    }
    response = await client.post(
        "/api/v1/auth/register",
        json=payload
    )

    data = response.json()
    assert response.status_code == 201
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]



@pytest.mark.asyncio
async def test_register_duplicate_email(client:AsyncClient, test_user):
    """Test registration with duplicate email."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email":test_user.email,
            "username":"differentuser",
            "password":"securepassword123"
        }

    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client:AsyncClient, test_user):
    """Test successful login."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email":test_user.email,
            "password":"Bonjour123@"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client:AsyncClient, test_user):
    """Test login with invalid credentials."""
    response = await client.post(
        "api/v1/auth/login",
        json={
            "email":test_user.email,
            "password":"wrongpassword"
        }
    )
    assert  response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client:AsyncClient, test_user):
    """Test token refresh."""
    # First login to get refresh token
    login_response = await client.post(
        "api/v1/auth/login",
        json={
            "email":test_user.email,
            "password":"Bonjour123@"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh the token
    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token":refresh_token
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"