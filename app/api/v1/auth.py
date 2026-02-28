from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas import UserCreate, TokenRequest, TokenResponse, TokenRefreshRequest, ErrorResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    responses={
        400:{"model":ErrorResponse, "description":"Email or username already exists"}
    }
)
async def register(
    user_data:UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """Register a new user account."""
    try:
        service = AuthService(session=session)
        result = await service.register_user(user_data=user_data)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
    
    
@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401:{"model":ErrorResponse, "description":"Invalid credentials"}
    }
)
async def login(
    credentials:TokenRequest,
    session: AsyncSession = Depends(get_session)
):
    """Login with email and password to receive JTW tokens."""
    try:
        service = AuthService(session=session)
        result = await service.authenticate_user(credentials.email, credentials.password)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
            
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
    
@router.post(
    "/refresh",
    response_model=dict,
    responses={
        401:{
            "model":ErrorResponse,
            "description":"Invalid refresh token"
        }
    }
)
async def refresh_token(
    request:TokenRefreshRequest,
    session: AsyncSession = Depends(get_session)
):
    """Refresh access token using refresh token."""
    service = AuthService(session=session)
    result = await service.refresh_access_token(request.refresh_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    return result
