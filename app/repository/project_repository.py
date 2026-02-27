from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.core.constants import ProjectStatusEnum


class ProjectRepository:
    """Project data access layer"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def create(
        self,
        name:str,
        owner_id: int,
        description:str | None = None,
        status: ProjectStatusEnum = ProjectStatusEnum.PLANNING
    ) -> Project:
        """Create a new project."""
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id,
            status=status
        )
        
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project
    
    
    
    async def get_by_id(self, project_id:int) -> Project | None:
        """Get project by ID.""" 
        stmt = select(Project).where(Project.id == project_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    
    async def get_user_projects(
        self,
        user_id:int,
        skip:int = 0,
        limit:int = 100
    ) -> list[Project]:
        """Get all projects owned by user."""
        stmt = (
            select(Project).where(Project.owner_id == user_id).offset(skip).limit(limit=limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    
    
    async def get_user_projects_count(
        self,
        user_id:int
    ) -> int:
        """Count user's projects"""
        stmt = select(func.count(Project.id)).where(Project.owner_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    
    
    async def get_projects_by_member(
        self,
        user_id:int,
        skip:int = 0,
        limit:int = 100
    ) -> list[Project]:
        """Get projects where user is a member."""
        stmt = (
            select(Project)
            .join(ProjectMember, Project.id==ProjectMember.project_id)
            .where(ProjectMember.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    
    
    async def update(
        self,
        project_id,
        **kwargs
    ) -> Project | None:
        """Update project fields"""
        project = await self.get_by_id(project_id=project_id)
        if not project:
            return None
        for key, item in kwargs.items():
            if hasattr(project,key):
                setattr(project,key,item)
                
        await self.session.commit()
        await self.session.refresh(project)
        return project
    
    
    
    async def delete(
        self,
        project_id: int
    ) -> int:
        """Delete project and cascade"""
        project = await self.get_by_id(project_id=project_id)
        if not project:
            return False
        
        await self.session.delete(project)
        await self.session.commit()
        return True
        
    
    
    
        
        