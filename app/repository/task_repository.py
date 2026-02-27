from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from app.models.task import Task
from app.core.constants import TaskStatusEnum, TaskPriorityEnum

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(
        self,
        title:str,
        project_id:int,
        description:str | None = None,
        priority:TaskPriorityEnum = TaskPriorityEnum.MEDIUM,
        assignee_id:int | None = None,
        due_date = None
    ) -> Task:
        """Create a new Task"""
        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            priority=priority,
            assignee_id=assignee_id,
            due_date=due_date
        )
        self.session.add(task)
        await  self.session.commit()
        await  self.session.refresh(task)
        return task
    
    
    
    async def get_by_id(
        self,
        task_id:int
    ) -> Task | None:
        """Get task by ID"""
        stmt = select(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    
    async def get_project_tasks(
        self,
        project_id:int,
        skip:int = 0,
        limit:int = 100,
        status:TaskStatusEnum | None = None
    ) -> list[Task]:
        """Get all tasks in a project with optional status filter."""
        stmt = select(Task).where(Task.project_id == project_id)
        
        if status:
            stmt = stmt.where(Task.status == status)
            
        stmt = stmt.offset(skip).limit(limit=limit).order_by(desc(Task.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    
    
    async def get_project_task_count(
        self,
        project_id:int,
        status:TaskStatusEnum | None = None
    ) -> int:
        """Count tasks in a project."""
        stmt = select(func.count(Task.id)).where(Task.project_id == project_id)
        
        if status:
            stmt = stmt.where(Task.status == status )
            
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    
    
    async def get_user_assigned_tasks(
        self,
        user_id:int,
        skip:int = 0,
        limit:int = 100,
        status:TaskStatusEnum | None = None
    ) -> list[Task]:
        """Get all tasks assigned to a user."""
        stmt = select(Task).where(Task.assignee_id == user_id)
        
        if status:
            stmt = stmt.where(Task.status == status)
        
        stmt = stmt.offset(skip).limit(limit=limit).order_by(desc(Task.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    
    
    async def update(
        self,
        task_id: int,
        **kwargs
    ) -> Task | None:
        """Delete a task."""
        task = await self.get_by_id(task)
        if not task:
            return None
        
        for key, value in kwargs.items():
            if hasattr(task,key):
                setattr(task,key,value)
                
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    
    
    
    async def delete(
        self,
        task_id:int
    ) -> bool:
        """Delete a task."""
        task = await self.get_by_id(task_id=task_id)
        if not task:
            return None
        
        await self.session.delete(task)
        await self.session.commit()
        return True
    
    
    
    async def bulk_update_status(
        self,
        project_id:int,
        from_status: TaskStatusEnum,
        to_status: TaskStatusEnum
    ) -> int:
        """Update all tasks with a given status in a project."""
        stmt = (
            select(Task).where(and_(Task.project_id == project_id,
                                    Task.status == from_status))
        )
        result = await self.session.execute(stmt)
        tasks = result.scalars().all()
        
        for task in tasks:
            task.status = to_status
            
        await self.session.commit()
        return len(tasks)
        