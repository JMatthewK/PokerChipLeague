from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

async def get_or_create_cognito_user(
    # The database session to use for the query and potential creation of a new user.
    db: AsyncSession,
    user_info: dict,
) -> User:
    """
    Find an application user by Cognito sub.

    If no matching database user exists, create one from
    the authenticated Cognito user information.
    """

    # Define variables for the Cognito sub and email from the user_info dictionary.
    cognito_sub = user_info.get("sub")
    email = user_info.get("email")

    if not cognito_sub:
        raise ValueError("Cognito response is missing the sub claim")

    if not email:
        raise ValueError("Cognito response is missing the email claim")

    statement = select(User).where(
        User.cognito_sub == cognito_sub
    )

    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    # Assign display_name based on available user information, falling back to the email prefix if necessary.
    display_name = (
        user_info.get("cognito:nickname")
        or user_info.get("cognito:username")
    )

    if user is None:
        user = User(
            cognito_sub=cognito_sub,
            email=email,
            display_name=display_name,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    changed = False

    if user.email != email:
        user.email = email
        changed = True

    if not user.display_name and display_name:
        user.display_name = display_name
        changed = True

    if changed:
        await db.commit()
        await db.refresh(user)

    return user