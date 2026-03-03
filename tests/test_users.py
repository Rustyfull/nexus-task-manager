import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user(client:AsyncClient, test_token, test_user):
    """Test getting current user info."""
    response = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email



@pytest.mark.asyncio
async def test_get_user_unauthorized(client:AsyncClient):
    """TEst accessing protected endpoint without token."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_users_admin_only(client:AsyncClient, test_token, admin_token):
    """Test that only admins can list users."""
    # Regular user should be denied
    response = await client.get(
        "/api/v1/users",
        headers={"Authorization":f"Bearer {test_token}"}

    )
    assert response.status_code == 403

    # Admin should succeed
    response = await client.get(
        "/api/v1/users",
        headers={"Authorization":f"Bearer {admin_token}"}
    )

    assert response.status_code == 200



@pytest.mark.asyncio
async def test_update_user_profile(client:AsyncClient, test_token, test_user):
    """Test updating user profile."""
    response = await client.put(
        f"/api/v1/users/{test_user.id}",
        headers={
            "Authorization":f"Bearer {test_token}"
        },
        json={
            "full_name" :"Updated Name"
        }

    )
    assert response.status_code == 200
    print("RESPONSE",response.json())
    assert response.json()["full_name"] == "Updated Name"



@pytest.mark.asyncio
async  def  test_cannot_update_user_profile(client:AsyncClient, test_token, test_db):
    """Test that users can#t update other user profiles."""
    # Create another user
    async with test_db() as session:
        from app.models.user import  User
        from app.core.security import get_security_service

        user2 = User(
            email="user2@example.com",
            username="user2",
            hashed_password=get_security_service().hashpassword("password123")
        )

        session.add(user2)
        await session.commit()
        await session.refresh(user2)
        other_user_id = user2.id

    response = await client.put(
        f"/api/v1/users/{other_user_id}",
        headers={"Authorization":f"Bearer {test_token}"},
        json={
            "full_name":"Hacked Name"
        }
    )

    assert response.status_code == 403