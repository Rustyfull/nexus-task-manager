from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user_repository import UserRepository
from app.core.constants import RoleEnum


class UserService:
    """User business logic layer."""
    
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session=session)
        
        
    async def get_user(
        self,
        user_id: int
    ):
        """Get user details."""
        return await self.repo.get_by_id(user_id=user_id)
    
    
    async def list_users(
        self,
        skip:int = 0,
        limit:int = 100
    ):
        """List all users with pagination."""
        users = await self.repo.list_all(skip=skip, limit=limit)
        total = await self.repo.count_all()
        
        return {
            "total":total,
            "skip":skip,
            "limit":limit,
            "items":users
        }
        
        
    
    async def update_user_profile(
        self,
        user_id:int,
        **kwargs
    ):
        """Update user profile fields."""
        # Whitelist allowed fields
        allowed_fields = {"full_name"}
        filtered_kwargs = {
            k:v for k, v in kwargs.items() if k in allowed_fields and v is not None
        }    
        
        if not filtered_kwargs:
            return await self.repo.get_by_id(user_id=user_id)
        
        return await self.repo.update(user_id=user_id,**filtered_kwargs)
    
    
    
    async def promote_user_to_admin(self, user_id: int):
        """Promote user to admin (admin only action)."""
        return await self.repo.update(user_id=user_id,role=RoleEnum.ADMIN)
    
    
    async def deactivate_user(self, user_id:int):
        """Deactivate user account."""
        return await self.repo.delete(user_id=user_id)
    
    
