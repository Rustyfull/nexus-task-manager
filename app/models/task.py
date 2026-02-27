from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SQLEnum, DateTime, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import TaskPriorityEnum, TaskStatusEnum


class Task(BaseModel):
    """Task model representing work items within projects."""
    
    __tablename__ = "tasks"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(SQLEnum(TaskStatusEnum), default=TaskStatusEnum.OPEN, nullable=False)
    priority = Column(SQLEnum(TaskPriorityEnum), default=TaskPriorityEnum.MEDIUM, nullable=False)
    due_date = Column(DateTime, nullable=True)
    
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
    
    
    __table_args__ = {
        Index("ix_task_project_status", "project_id", "status"),
        Index("ix_task_assignee", "assignee_id"),
        Index("ix_task_due_date", "due_date")
    }