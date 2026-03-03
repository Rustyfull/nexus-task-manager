from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.api.dependencies import get_current_user
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import ProjectService
from app.core.constants import ERROR_MESSAGES

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
        project_data:ProjectCreate,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Create a new project."""
    service = ProjectService(session)
    project = await service.create_project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id
    )
    return project



@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
        project_id:int,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Get project details."""
    service = ProjectService(session)
    has_access = await service.verify_project_access(project_id,current_user.id, current_user.role)

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this project"
        )
    project = await service.get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project Not found"
        )

    return project



@router.get("",response_model=dict)
async def list_user_projects(
        skip:int = 0,
        limit: int = 100,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """List all projects owned by current user."""
    limit = min(limit,100)
    service = ProjectService(session)
    return await service.list_user_projects(current_user.id,skip,limit)




@router.put("/{project_id}",response_model=ProjectResponse)
async def update_project(
        project_id:int,
        project_data: ProjectUpdate,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Update project details."""
    service = ProjectService(session)

    try:
        project = await service.update_project(
            project_id,
            owner_id=current_user.id,
            user_role=current_user.role,
            **project_data.model_dump(exclude_unset=True)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project





@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async  def delete_project(
        project_id:int,
        session: AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Delete a project."""
    service = ProjectService(session)

    try:
        result = await service.delete_project(
            project_id,
            owner_id=current_user.id,
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
            detail="Project not found"
        )

