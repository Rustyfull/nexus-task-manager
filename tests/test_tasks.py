from pickletools import read_stringnl_noescape_pair

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client:AsyncClient, test_token, test_db, test_user):
    """Test creating a task."""
    # Create project first
    async with test_db() as session:
        from app.models.project import Project

        project = Project(
            name="Test Project",
            owner_id=test_user.id
        )

        session.add(project)
        await session.commit()
        await session.refresh(project)
        project_id = project.id

    response = await client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers={
            "Authorization":f"Bearer {test_token}"
        },
        json={
            "title":"Test Task",
            "description":"A test task",
            "priority":"high"
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"



@pytest.mark.asyncio
async def test_create_task_unauthorized_project(client:AsyncClient, test_token, test_db, test_user):
    """Test creating task in unauthorized project."""
    # Create project owned by different user
    async with test_db() as session:
        from app.models.project import Project
        from app.models.user import User
        from app.core.security import get_security_service

        other_user = User(
            email="other@example.com",
            username="other",
            hashed_password=get_security_service().hashpassword("pass123")
        )
        session.add(other_user)
        await session.commit()

        project = Project(
            name="Other User Project",
            owner_id=other_user.id
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        project_id = project.id

    response = await client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers={
            "Authorization":f"Bearer {test_token}",

        },
        json={
            "title":"Hacked Task"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_project_tasks(client:AsyncClient, test_token,test_db,test_user):
    """Test listing tasks in a project."""
    # Create project and tasks
    async with test_db() as session:
        from app.models.project import  Project
        from app.models.task import Task

        project = Project(
            name="Test Project",
            owner_id=test_user.id
        )
        session.add(project)
        await session.commit()

        for i in range(3):
            task = Task(
                title=f"Task {i}",
                project_id=project.id
            )
            session.add(task)
        await session.commit()
        await session.refresh(project)
        project_id = project.id

    response = await client.get(
        f"/api/v1/projects/{project_id}/tasks",
        headers={
            "Authorization":f"Bearer {test_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["total"] == 3


@pytest.mark.asyncio
async def test_update_task_by_assignee(client:AsyncClient, test_token, test_db, test_user):
    """Test that assignee can update task."""
    # Create project and task
    async  with test_db() as session:
        from app.models.project import  Project
        from app.models.task import Task

        project = Project(
            name="Test Project",
            owner_id=test_user.id
        )
        session.add(project)
        await session.commit()

        task = Task(
            title="Test Task",
            project_id=project.id,
            assignee_id=test_user.id
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        task_id = task.id
        project_id = project.id


    response = await client.put(
        f"/api/v1/projects/{project_id}/tasks/{task_id}",
        headers={
            "Authorization":f"Bearer {test_token}"
        },
        json={
            "status":"in_progress"
        }

    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"



@pytest.mark.asyncio
async def test_delete_task(client:AsyncClient, test_token, test_db, test_user):
    """Test deleting a task."""
    # Create project and task
    async with test_db() as session:
        from app.models.project import Project
        from app.models.task import Task

        project = Project(
            name="Test Project",
            owner_id=test_user.id
        )
        session.add(project)
        await session.commit()

        task = Task(
            title="Task to Delete",
            project_id=project.id
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        task_id = task.id
        project_id = project.id

    response = await client.delete(
        f"/api/v1/projects/{project_id}/tasks/{task_id}",
        headers={
            "Authorization":f"Bearer {test_token}"
        }
    )
    assert response.status_code == 204
