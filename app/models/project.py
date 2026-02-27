from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import ProjectStatusEnum

class Project(BaseModel):
    """Project model representing a task collection"""
    __tablename__ = "projects"
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(ProjectStatusEnum), default=ProjectStatusEnum.PLANNING, nullable=False)
    
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete orphan")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    
    
    __table_args__ = (
        Index("ix_project_owner_status", "owner_id", "status")
    )