from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Creates a new database session for each request and ensures that the session is closed after the request is completed.

    Returns:
        AsyncGenerator[AsyncSession, None]: An asynchronous generator that yields a database session for each request.
    Yields:
        Iterator[AsyncGenerator[AsyncSession, None]]: An iterator that yields a database session for each request.
    """
    async with AsyncSessionLocal() as session:
        yield session