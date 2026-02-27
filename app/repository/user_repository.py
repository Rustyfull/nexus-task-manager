from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.core.constants import RoleEnum

class UserRepository:
    """User data access layer."""
    def __init__(self, session:AsyncSession):
        self.session = session
        
    async def create(
        self,
        email:str,
        username:str,
        hashed_password:str,
        full_name:str | None = None,
        role:RoleEnum = RoleEnum.USER
    ) -> User:
        """Create a new user."""
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role
        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    
    
    
    async def get_by_id(self,user_id:int) -> User | None:
        """Get user by ID."""
        stmt = select(User).where(User.id == user_id).wher(User.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        stmt = select(User).where(User.email == email).where(User.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    
    async def get_by_username(self, username: str) -> User | None:
        """Get user by username."""
        stmt = select(User).where(User.username == username).where(User.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    
    async def update(self, user_id:int, **kwargs) -> User | None:
        """Update user fields."""
        user = await self.get_by_id(user_id=user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user,key,value)
                
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    
    
    
    async def delete(self, user_id:int) -> bool:
        """Soft delete user."""
        user = self.get_by_id(user_id=user_id)
        if not user:
            return False
        
        user.is_active = False
        await self.session.commit()
        return True
    
    
    async def list_all(self, skip:int = 0, limit:int = 100) -> list[User]:
        """List all active users with pagination"""
        stmt = (
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        
        result =  await self.session.execute(stmt)
        return result.scalars().all()    
    
    
    def count_all(self) -> int:
        """Count total active users."""
        stmt = select(func.count(User.id)).where(User.is_active == True)
        result = await self.session.execute(stmt)
        return result