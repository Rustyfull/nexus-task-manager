import pytest
from httpx import AsyncClient

from tests.conftest import test_db


@pytest.mark.asyncio
async def test_create_project(client:AsyncClient, test_token, test_user):
    """Test creating a project"""
    response = await client.post(
        "/api/v1/projects",
        headers={"Authorization":f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
    assert response.json()["owner_id"] == test_user.id



@pytest.mark.asyncio
async def test_create_project_unauthorized(client:AsyncClient):
    """Test creating project without auth."""
    response = await client.post(
        "/api/v1/projects",
        json={
            "name":"Test",
            "description":"Test"
        }
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_project(client:AsyncClient, test_token,test_db, test_user):
    """Test retrieving a project."""
    # Create a project
    async with test_db() as session:
        from app.models.project import Project

        project = Project(
            name="Test Project",
            description="Test",
            owner_id=test_user.id
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        project_id = project.id

    response = await client.get(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization":f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"



@pytest.mark.asyncio
async def test_list_user_projects(
        client:AsyncClient,
        test_token,
        test_db,
        test_user
):
    """Test listing user's projects."""
    # Create projects
    async with test_db() as session:
        from app.models.project import Project

        for i in range(3):
            project = Project(
                name=f"Project {i}",
                owner_id=test_user.id
            )
            session.add(project)
        await session.commit()

    response = await client.get(
        "/api/v1/projects",
        headers={"Authorization":f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["total"] == 3


@pytest.mark.asyncio
async def test_update_project(client:AsyncClient, test_token, test_db, test_user):
    """Test updating a project."""
    # Create project
    async with test_db() as session:
        from app.models.project import  Project

        project = Project(
            name="Old Name",
            owner_id=test_user.id
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        project_id = project.id


    response = await client.put(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization":f"Bearer {test_token}"},
        json={
            "name":"New Name"
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"




@pytest.mark.asyncio
async def test_delete_project(client:AsyncClient, test_token, test_db, test_user):
    """Test deleting a project."""
    # Create project
    async with test_db() as session:
        from app.models.project import Project

        project = Project(
            name="To Delete",
            owner_id=test_user.id
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        project_id = project.id

    response = await client.delete(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert  response.status_code == 204
