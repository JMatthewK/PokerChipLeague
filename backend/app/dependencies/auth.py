import uuid

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.models.user import User


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Return the authenticated database user."""

    session_user = request.session.get("user")

    if not session_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    try:
        user_id = uuid.UUID(session_user["id"])
    except (KeyError, TypeError, ValueError):
        request.session.clear()

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication session",
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        request.session.clear()

        raise HTTPException(
            status_code=401,
            detail="Authenticated user no longer exists",
        )

    return user