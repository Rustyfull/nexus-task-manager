import  pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import  AsyncClient
from app.main import create_app
from app.core.database import get_session
from app.models.base import Base
from app.core.security import get_security_service
from app.core.constants import  RoleEnum


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async  def test_db():
    """Create test database."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread":False},
        poolclass=None
    )

    async  with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


    async  def override_get_session():
        async  with AsyncSessionLocal() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session

    yield  AsyncSessionLocal


    async  with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()



@pytest_asyncio.fixture
async def client(test_db):
    """Create test client."""
    app = create_app()

    async def override_get_session():
        async  with test_db() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://client") as ac:
        yield ac


@pytest_asyncio.fixture
async  def test_user(test_db):
    """Create test user."""
    async with test_db() as session:
        from app.models.user import  User

        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_security_service().hashpassword("Bonjour123@"),
            full_name="Test User",
            role=RoleEnum.USER,
            is_active=True,
            is_verified=True
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user



@pytest_asyncio.fixture
async  def test_admin_user(test_db):
    """Create test admin user."""
    async with test_db() as session:
        from app.models.user import  User


        user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_security_service().hashpassword("Bonjour123@"),
            full_name="Admin User",
            role=RoleEnum.ADMIN,
            is_active=True,
            is_verified=True
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user



@pytest_asyncio.fixture
def test_token(test_user):
    """Create test JWT token."""
    token_data = {
        "sub":str(test_user.id),
        "email":test_user.email,
        "role":test_user.role
    }
    return get_security_service().create_access_token(token_data)



@pytest_asyncio.fixture
def admin_token(test_admin_user):
    """Create test JWT-token for admin."""
    token_data = {
        "sub":str(test_admin_user.id),
        "email":test_admin_user.email,
        "role":test_admin_user.role
    }
    return get_security_service().create_access_token(token_data)