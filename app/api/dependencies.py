from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import get_security_service
from app.repository.user_repository import UserRepository
from app.core.constants import ERROR_MESSAGES, RoleEnum



security = HTTPBearer()

async def get_current_user(
    credentials:HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
):
    """Dependency to get authenticated user from JWT token."""
    token = credentials.credentials
    payload = get_security_service().decode_token(token=token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES["TOKEN_EXPIRED"],
            headers={"WWW-Authenticate":"Bearer"}
        )
        
        
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES["UNAUTHORIZED"],
            headers={"WWW-Authenticate":"Bearer"}   
        )
        
    repo = UserRepository(session=session)
    user = await repo.get_by_id(int(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES["UNAUTHORIZED"],
            headers={"WWW-Authenticate":"Bearer"}
        )
        
    return user



async def get_admin_user(
    current_user=Depends(get_current_user)
):
    """Dependency to ensure user is admin"""
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES["FORBIDDEN"]
        )
    return current_user



def require_role(*roles:RoleEnum):
    """Dependency factory to require specific roles."""
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_MESSAGES["FORBIDDEN"]
            )
        return current_user
    return role_checker
