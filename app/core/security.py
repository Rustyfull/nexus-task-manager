from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
settings = get_settings()

class SecurityService:
    """Handles JWT token generation, validation, and password management."""
    
    @staticmethod
    def hashpassword(password:str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verifypassword(plain_password:str, hashed_password:str) -> bool:
        """Verify a plain password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta:Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta (
                minutes=settings.access_token_expire_minutes
            )
        to_encode.update(
            {
                "exp":expire,
                "type":"access"
            }
        )
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    
    
    @staticmethod
    def create_refresh_token(data:dict) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
        to_encode.update(
            {
                "exp":expire,
                "type":"refresh"
            }
        )
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
            
        )
        
        return encoded_jwt
    
    
    @staticmethod
    def decode_token(token:str) -> Optional[dict]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.encode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            return payload
        except JWTError:
            return None
        
        
        
        
def get_security_service() -> SecurityService:
    return SecurityService()