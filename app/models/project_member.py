from sqlalchemy import Column, Integer, ForeignKey, String, Enum as SQLEnum, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ProjectMember(BaseModel):
    """Project membership model linking users to projects."""
    __tablename__ = "project_members"
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), default="member", nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")
    
    
    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="uq_project_user"),
        Index("ix_member_project","project_id"),
        Index("ix_member_user", "user_id")
    )