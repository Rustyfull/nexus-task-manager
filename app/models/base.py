from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base
import pytz

Base = declarative_base()

class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps to models."""
    
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.UTC),
        nullable=False
    )
    
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.UTC),
        nullable=False
    )
    
    
class BaseModel(Base,TimestampMixin):
    """Abstract base model for all database models."""
    __abstract__ = True
    id = Column(Integer, primary_key=True,index=True)