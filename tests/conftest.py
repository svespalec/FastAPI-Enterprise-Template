import asyncio
from typing import AsyncGenerator

import asyncpg
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import Base, get_session
from app.main import app

# Test database name - extract from DATABASE_URL or use default
TEST_DB_NAME = settings.DATABASE_URL.split("/")[-1]

# Test database URL - use as is since it already contains the test database name
TEST_DATABASE_URL = settings.DATABASE_URL

# For CI environment, use localhost instead of container name
DB_HOST = "localhost" if settings.DATABASE_URL.find("localhost") != -1 else "db"


async def create_test_database():
    """Create test database if it doesn't exist."""
    try:
        # Connect to default database first
        conn = await asyncpg.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host=DB_HOST,
        )
        # Drop test database if it exists and create it fresh
        await conn.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
        await conn.execute(f"CREATE DATABASE {TEST_DB_NAME}")
        await conn.close()
        # Verify we can connect to the test database
        test_conn = await asyncpg.connect(
            database=TEST_DB_NAME,
            user="postgres",
            password="postgres",
            host=DB_HOST,
        )
        await test_conn.close()
    except Exception as e:
        print(f"Error setting up test database: {e}")
        raise


# Create async engine for tests
engine_test = create_async_engine(
    TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    poolclass=NullPool,
)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


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
    # Create test database and tables
    await create_test_database()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield app
    # Clean up - drop all tables
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
