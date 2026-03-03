from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.api.dependencies import get_current_user, get_admin_user
from app.schemas import UserResponse
from app.core.constants import ERROR_MESSAGES
from app.services.user_service import  UserService

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/me",response_model=UserResponse)
async def get_current_user_info(
        current_user=Depends(get_current_user)
):
    """Get current authenticated user information."""
    return current_user


@router.get("/{user_id}",response_model=UserResponse)
async def get_user(
        user_id:int,
        session: AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)
):
    """Get user details (users can only view their own profile, admins can view all)."""
    if user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES["FORBIDDEN"]
        )

    service  = UserService(session)
    user = await service.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["NOT_FOUND"]
        )

    return  user



@router.get("", response_model=dict)
async def list_users(
        skip:int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_session),
        current_user = Depends(get_admin_user)
):
    """List all users (admin only)."""
    limit = min(limit,100) # Max per page
    service = UserService(session)
    return await service.list_users(skip=skip,limit=limit)




@router.put("/{user_id}",response_model=UserResponse)
async def update_user_profile(
        user_id: int,
        full_name:str | None = None,
        session: AsyncSession = Depends(get_session),
        current_user = Depends(get_current_user)

):
    """Update user profile (users can only update their own profile)-"""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES["UNAUTHORIZED"]
        )
    service = UserService(session)
    user = await service.update_user_profile(user_id,full_name=full_name)

    return user



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
        user_id:int,
        session:AsyncSession = Depends(get_session),
        current_user = Depends(get_admin_user)
):
    """Deactivate user account (admin only)"""
    service = UserService(session)
    result = await service.deactivate_user(user_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT_FOUND"
        )

