import asyncio
import pytest
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import asyncpg

from app.core.config import settings
from app.core.database import Base, get_session
from app.main import app

# Test database URL
TEST_DATABASE_URL = settings.DATABASE_URL + "_test"

async def create_test_database():
    """Create test database if it doesn't exist."""
    conn = await asyncpg.connect(
        database="fastapi_db",
        user="postgres",
        password="postgres",
        host="db"
    )
    
    try:
        await conn.execute("CREATE DATABASE fastapi_db_test")
    except asyncpg.exceptions.DuplicateDatabaseError:
        pass
    finally:
        await conn.close()

# Create async engine for tests
engine_test = create_async_engine(
    TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    poolclass=NullPool
)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_app():
    # Create test database
    await create_test_database()
    
    # Create tables
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield app
    
    # Clean up
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@pytest.fixture
async def client(test_app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
async def clean_tables():
    """Clean all tables before each test."""
    async with engine_test.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete()) 