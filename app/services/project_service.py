from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.project_repository import ProjectRepository
from app.core.constants import ProjectStatusEnum, RoleEnum


class ProjectService:
    """Project business logic layer"""
    
    def __init__(self, session: AsyncSession):
        self.repo = ProjectRepository(session=session)
        
        
    async def create_project(
        self,
        name:str,
        description:str | None,
        owner_id: int
    ):
        """Create a new project."""
        return await self.repo.create(
            name=name,
            owner_id=owner_id,
            description=description,
            status=ProjectStatusEnum.PLANNING
        )
        
        
    async def get_project(
        self,
        project_id: int
    ):
        """Get project details."""
        return await self.repo.get_by_id(project_id=project_id)
    
    
    async def list_user_projects(
        self,
        user_id:int,
        skip:int = 0,
        limit:int = 100
    ):
        """List projects owned by user."""
        projects = await self.repo.get_user_projects(user_id=user_id, skip=skip,limit=limit)
        total = await self.repo.get_user_projects_count(user_id=user_id)
        
        return {
            "total":total,
            "skip":skip,
            "limit":limit,
            "items":projects
        }
        
        
        
    async def update_project(
        self,
        project_id:int,
        owner_id:int,
        user_role:RoleEnum,
        **kwargs
    ):
        """Update project (authorization check)."""
        project = await self.repo.get_by_id(project_id=project_id)
        if not project:
            return None
        
        # Only owner or admin can update
        if project.owner_id != owner_id and user_role != RoleEnum.ADMIN:
            raise PermissionError("Not authorized to update this project")
        
        
        filtered_kwargs = {
            k:v for k, v in kwargs.items()
            if k in ["name", "description","status"] and v is not None
        }
        return await self.repo.update(project_id=project_id, **filtered_kwargs)
    
    
    
    
    async def delete_project(
        self,
        project_id: int,
        owner_id: int,
        user_role:RoleEnum
    ):
        """Delete project (authorization check)."""
        project = await self.repo.get_by_id(project_id=project_id)
        if not project:
            return False
        
        # Only owner or admin can delete
        if project.owner_id != owner_id and user_role != RoleEnum.ADMIN:
            raise PermissionError("Not authorized to delete this project")
        
        return await self.repo.delete(project_id=project_id)
    
    
    
    async def verify_project_access(
        self,
        project_id:int,
        user_id:int,
        user_role:RoleEnum
    ) -> bool:
        """Verify user has access to project."""
        project = await self.repo.get_by_id(project_id=project_id)
        if not project:
            return False
        
        # Owner or admin always has access
        if project.owner_id == user_id or user_role == RoleEnum.ADMIN:
            return True
        
        # Check if user is project member
        member_projects = await self.repo.get_projects_by_member(user_id=user_id)
        return any(p.id == project_id for p in member_projects)