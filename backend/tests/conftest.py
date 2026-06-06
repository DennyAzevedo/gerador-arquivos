import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from tests.support.db_url import resolve_test_database_url

os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
os.environ.setdefault("WORDPRESS_MOCK", "true")
os.environ.setdefault("WORDPRESS_URL", "https://exemplo.wordpress.com")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-for-pytest-min-32-chars")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")
os.environ["DATABASE_URL"] = resolve_test_database_url()

from app.core.config import get_settings

get_settings.cache_clear()

import app.infrastructure.db.models  # noqa: F401
import app.infrastructure.db.session as session_module
from app.infrastructure.db.base import Base

test_engine = create_async_engine(
    resolve_test_database_url(),
    poolclass=NullPool,
)
test_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

session_module.engine = test_engine
session_module.async_session_maker = test_session_maker

from app.main import app


_tables_initialized = False


@pytest.fixture
async def prepare_database() -> AsyncGenerator[None, None]:
    global _tables_initialized
    if not _tables_initialized:
        async with test_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
        _tables_initialized = True
    yield


async def _truncate_tables() -> None:
    async with test_session_maker() as session:
        await session.execute(text("TRUNCATE TABLE articles, users RESTART IDENTITY CASCADE"))
        await session.commit()


@pytest.fixture
async def client(prepare_database) -> AsyncGenerator[AsyncClient, None]:
    await _truncate_tables()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
async def db_session(prepare_database) -> AsyncGenerator[AsyncSession, None]:
    await _truncate_tables()
    async with test_session_maker() as session:
        yield session


@pytest.fixture
async def auth_headers(client: AsyncClient) -> dict[str, str]:
    email = "pytest-user@exemplo.com"
    password = "senhaSegura123"
    await client.post("/auth/register", json={"email": email, "password": password})
    login_response = await client.post(
        "/auth/jwt/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
