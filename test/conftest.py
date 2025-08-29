import pytest

from httpx import ASGITransport, AsyncClient
from core.database.db_helper import async_session_maker, engine
from core.database.models import Base
from core.config import settings
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as async_client:
        yield async_client
        
@pytest.fixture
async def session():
    async with async_session_maker() as session:
        yield session
        
@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    if settings.MODE == "TEST":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            
        yield 
            
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

