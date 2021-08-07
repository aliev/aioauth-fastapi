from typing import Optional
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


sqlalchemy_engine: Optional[AsyncEngine] = None


def get_sqlalchemy_async_session() -> sessionmaker:
    async_session = sessionmaker(
        sqlalchemy_engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session
