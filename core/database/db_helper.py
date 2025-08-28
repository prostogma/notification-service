from typing import Annotated
from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from core.config import settings

if settings.MODE == "TEST":
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
else:
    engine = create_async_engine(settings.DATABASE_URL)
    
async_session_maker = async_sessionmaker(engine)

async def create_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при работе с сессией - {e}")
            raise
    
session_DB = Annotated[AsyncSession, Depends(create_session)]
            