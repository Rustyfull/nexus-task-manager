from enum import Enum

class RoleEnum(str,Enum):
    """User roles for RBAC."""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    
    
    
class TaskStatusEnum(str, Enum):
    """Task status lifecycle"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
    
class TaskPriorityEnum(str,Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    
class ProjectStatusEnum(str,Enum):
    """Project lifecycle states."""
    PLANNING = "planning"
    ACTIVE  = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    
    
# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# Error messages
ERROR_MESSAGES = {
    "UNAUTHORIZED":"Not authenticated",
    "FORBIDDEN":"Insufficent permissions",
    "NOT_FOUND":"Resource not found",
    "DUPLICATE":"Resource already exists",
    "INVALID_CREDENTIALS":"Invalid credentials",
    "TOKEN_EXPIRED":"Token expired",
}