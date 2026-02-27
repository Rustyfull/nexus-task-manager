from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.core.constants import RoleEnum, TaskStatusEnum, TaskPriorityEnum, ProjectStatusEnum


# ========== Auth Schemas ==========
class TokenRequest(BaseModel):
    email:EmailStr
    password:str = Field(...,min_length=6)
    
class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str = "bearer"
    
    
class TokenRefreshRequest(BaseModel):
    refresh_token:str
    
    

# ========== User Schemas ==========
class UserCreate(BaseModel):
    email:EmailStr
    username: str  = Field(..., min_length=3, max_length=100)
    password:str  = Field(...,min_length=8)
    full_name:Optional[str] = None
    
    
class UserResponse(BaseModel):
    id:int
    email:str
    username:str
    full_name:Optional[str]
    role:RoleEnum
    is_active:bool
    is_verified:bool
    created_at:datetime
    updated_at:datetime
    
    
    class Config:
        from_attributes = True
        
        
        
# ========== Project Schemas ==========
class ProjectCreate(BaseModel):
    name:str = Field(..., min_length=1, max_length=255)
    description:Optional[str] = None
    
    
class ProjectUpdate(BaseModel):
    name:Optional[str] = None
    description:Optional[str] = None
    status: Optional[ProjectStatusEnum] = None
    

class ProjectResponse(BaseModel):
    id:int
    name:str
    description:Optional[str]
    status:ProjectStatusEnum
    owner_id:int
    created_at:datetime
    updated_at:datetime
    
    class Config:
        from_attributes = True
        
        
    
# ========== Task Schemas ==========
class TaskCreate(BaseModel):
    title:str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    due_date: Optional[datetime] = None
    assignee_id:Optional[str] = None
    
    
class TaskUpdate(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None
    status:Optional[TaskStatusEnum] = None
    priority:Optional[TaskPriorityEnum] = None
    due_date: Optional[datetime] = None
    assignee_id:Optional[int] = None
    
    
class TaskResponse(BaseModel):
    id:int
    title:str
    description:Optional[str]
    status:TaskStatusEnum
    priority:TaskPriorityEnum
    project_id:int
    assignee_id:Optional[id]
    due_date:Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    
    class Config:
        from_attributes = True
        
        

# ========== ProjectMember Schemas ==========
class ProjectMemberCreate(BaseModel):
    user_id:int
    role:str = "member"
    
    
class ProjectMemberResponse(BaseModel):
    id:int
    project_id:int
    user_id:int
    role:str
    created_at:datetime
    
    
    class Config:
        from_attributes = True
        
        

# ========== Error Schemas ==========
class ErrorResponse(BaseModel):
    detail:str
    error_code:Optional[str] = None
    
    
class ValidationErrorResponse(BaseModel):
    detail:list[dict]