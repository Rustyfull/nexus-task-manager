from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.database import  get_session
from app.api.dependencies import get_current_user
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.core.constants import TaskStatusEnum

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
        project_id:int,
        task_data: TaskCreate,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Create a new task in a project."""
    service = TaskService(session)

    try:
        task = await service.create_task(
            title=task_data.title,
            project_id=project_id,
            user_id=current_user.id,
            user_role=current_user.role,
            description=task_data.description,
            priority=task_data.priority,
            assignee_id=task_data.assignee_id,
            due_date=task_data.due_date
        )
        return task
    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST if isinstance(e,ValueError) else status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        project_id: int,
        task_id: int,
        session: AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Get task details."""
    service = TaskService(session)

    try:
        # Verify project access first
        from app.services.project_service import  ProjectService
        project_service = ProjectService(session)
        has_access = await project_service.verify_project_access(
            project_id,
            current_user.id,
            current_user.role
        )

        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this project"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this project"
        )

    task  = await service.get_task(task_id)

    if not task or task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return  task


@router.get("",response_model=dict)
async def list_project_tasks(
        project_id: int,
        skip: int = 0,
        limit: int = 100,
        status_filter: TaskStatusEnum | None = Query(None,alias="status"),
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """List all tasks in a project with optional status filter."""
    limit = min(limit, 100)
    service = TaskService(session)

    try:
        return await service.list_project_tasks(
            project_id,
            current_user.id,
            current_user.role,
            skip,
            limit,
            status_filter,

        )
    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN if isinstance(e, ValueError) else status.HTTP_404_NOT_FOUND,
            detail=str(e)

        )



@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        project_id:int,
        task_id:int,
        task_data: TaskUpdate,
        session: AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Update task details."""
    service = TaskService(session)

    try:
        task = await service.update_task(
            task_id,
            user_id=current_user.id,
            user_role=current_user.role,
            **task_data.model_dump(exclude_unset=True)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    if not task or task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found!"
        )

    return task



@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id:int,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Delete a task."""
    service = TaskService(session)

    try:
        result = await  service.delete_task(
            task_id=task_id,
            user_id=current_user.id,
            user_role=current_user.role

        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )