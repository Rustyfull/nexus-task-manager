from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import RoleEnum

class User(BaseModel):
    """User model with role-based access control."""
    __tablename__ = "users"
    
    email = Column(String(255),unique=True,nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.USER,nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    