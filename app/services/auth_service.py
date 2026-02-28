from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user_repository import UserRepository
from app.core.security import get_security_service
from app.core.constants import RoleEnum, ERROR_MESSAGES
from app.schemas import UserCreate, TokenResponse



class AuthService:
    """Authentication business logic layer."""
    
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session=session)
        
    
    async def register_user(
        self,
        user_data:UserCreate
    ) -> dict:
        """Register a new user."""
        # Check if email already exists
        existing_user = await self.repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Check if username already exists
        existing_username = await self.repo.get_by_username(user_data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        
        # Hash password and create user
        hashed_password = get_security_service().hashpassword(user_data.password)
        user  = await self.repo.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=RoleEnum.USER
        )
        
        return {
            "user_id":user.id,
            "email":user.email,
            "username":user.username
        }
        
        
        
    async def authenticate_user(
            self,
            email:str,
            password: str
     ) -> dict | None:
        """Authenticate user and return tokens."""
        user = await self.repo.get_by_email(email)
            
        if not user or not get_security_service().verifypassword(password,user.hashed_password):
            return None
        
        if not user.is_active:
            raise ValueError("User account is deactivated")
        
        # Create tokens
        token_data = {"sub":str(user.id), "email":user.email, "role":user.role}
        access_token = get_security_service().create_access_token(token_data)
        refresh_token = get_security_service().create_refresh_token(token_data)
        
        return {
            "access_token":access_token,
            "refresh_token":refresh_token,
            "token_type":"bearer"
        }
        
        
    async def refresh_access_token(
        self,
        refresh_token: str
    ) -> dict | None:
        """Generate new access token from refresh token."""
        payload = get_security_service().decode_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            return None
    
        user_id = int(payload.get("sub"))
        user = await self.repo.get_by_id(user_id=user_id)
        
        if not user:
            return None
        
        token_data = {
            "sub":str(user.id),
            "email":user.email,
            "role":user.role
        }
        
        access_token = get_security_service().create_access_token(token_data)
        
        return {
            "access_token":access_token,
            "token_type":"bearer"
        }
        
        