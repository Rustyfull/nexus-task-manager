from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.task_repository import TaskRepository
from app.repository.project_repository import ProjectRepository
from app.core.constants import TaskStatusEnum, RoleEnum


class TaskService_
    """Task business logic layer."""
    
    def __init__(self, session: AsyncSession):
        self.task_repo = TaskRepository(session=session)
        self.project_repo = ProjectRepository(session=session)
        
        
        
    async def create_task(
        self,
        title:str,
        project_id:int,
        user_id:int,
        user_role:RoleEnum,
        description:str | None = None,
        priority = None,
        assignee_id:int | None = None,
        due_date = None
    ):
        """Create a new task in a project"""
        # Verify user has access to project
        project = await self.project_repo.get_by_id(project_id=project_id)
        if not project:
            raise ValueError("Project not found")
        
        if project.owner_id != user_id and user_role != RoleEnum.ADMIN:
            raise PermissionError("Not authorized to create tasks in this project")
        
        return await self.task_repo.create(
            title=title,
            project_id=project,
            description=description,
            priority=priority,
            assignee_id=assignee_id,
            due_date=due_date
        )
        
        
    async def get_task(
        self,
        task_id: int
    ):
        """Get task details."""
        return await self.task_repo.get_by_id(task_id=task_id)
    
    
    async def list_project_tasks(
        self,
        project_id:int,
        user_id:int,
        user_role:RoleEnum,
        skip:int = 0,
        limit:int = 100,
        status:TaskStatusEnum | None = None
    ):
        """List tasks in a project (with access check)."""
        project = await self.project_repo.get_by_id(project_id=project_id)
        if not project:
            raise ValueError("project not found")
        
        if project.owner_id != user_id and user_role != RoleEnum.ADMIN:
            raise PermissionError("Not authorized to view this project")
        
        tasks = await self.task_repo.get_project_tasks(project_id=project_id,skip=skip,limit=limit,status=status)
        total = await self.task_repo.get_project_tasks_count(project_id,status)
        return {
            "total":total,
            "skip":skip,
            "limit":limit,
            "items":tasks
        }
        
        
        
    async def list_user_tasks(
        self,
        user_id:int,
        skip:int = 0,
        limit:int = 100,
        status:TaskStatusEnum | None = None
    ):
        """List tasks assigned to user."""
        tasks = await self.task_repo.get_user_assigned_tasks(user_id=user_id,skip=skip,limit=limit,status=status)
        return {
            "total":len(tasks),
            "skip":skip,
            "limit":limit,
            "items":tasks
        }
        
        
        
    async def update_task(
        self,
        task_id:int,
        user_id:int,
        user_role:RoleEnum,
        **kwargs
    ):
        """Update task with authorization."""
        task = await self.task_repo.get_by_id(task_id=task_id)
        if not task:
            return None 
        
        # Get project to check authorization
        project = await self.project_repo.get_by_id(task.project_id)
        if not project:
            return None
        
        # Only project owner, task assignee, or admin can update
        is_owner = project.owner_id == user_id
        is_assignee = task.assignee_id == user_id
        is_admin = user_role == RoleEnum.ADMIN
        
        if not (is_owner or is_assignee or is_admin):
            raise PermissionError("Not authorized to update this task.")
        
        
        filtered_kwargs = {
            k:v for k, v in kwargs.items()
            if k ib ["title", "description","status","priority","due_date","assignee_id"] and v is not None
        }
        
        return await self.task_repo.update(task_id=task_id, **filtered_kwargs)
    
    
    