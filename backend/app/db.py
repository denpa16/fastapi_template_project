from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"


class AsyncSessionBuilder:
    def __init__(self, database_url: str, echo=False):
        self.database_url = database_url
        self.engine = create_async_engine(database_url, echo=echo)

    def __call__(self, *args, **kwargs) -> async_sessionmaker:
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)
        return self.session


session_builder = AsyncSessionBuilder(database_url=DATABASE_URL, echo=True)


async def get_db_session() -> AsyncSession:
    async_session: async_sessionmaker = session_builder()
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()

        await session.commit()


async_session: AsyncSession = Depends(get_db_session)
