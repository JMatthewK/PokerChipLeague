# Working with the Leagues Table from Supabase, Routing it to our FastAPI backend.
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.league import League
from app.models.league_membership import LeagueMembership
from app.models.user import User
from app.schemas.league import LeagueCreate, LeagueResponse

router = APIRouter(
    prefix="/leagues",
    tags=["Leagues"]
)

# Router call to create a league based on user input, and the current authenticated user. The league is created with the provided name and starting chip balance, and the authenticated user is set as the owner of the league. The owner is also added as the first member of the league with an active status and the starting chip balance.
@router.post(
    "",
    response_model=LeagueResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_league(
    payload: LeagueCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a league for the authenticated user.

    The authenticated user becomes both the league owner
    and the first league member.
    """

    league = League(
        name=payload.name.strip(),
        status="active",
        owner_user_id=current_user.id,
        starting_chip_balance=payload.starting_chip_balance,
    )

    db.add(league)

    try:
        # Sends the INSERT without committing, allowing PostgreSQL
        # to generate the league UUID.
        await db.flush()

        owner_membership = LeagueMembership(
            league_id=league.id,
            user_id=current_user.id,
            role="owner",
            status="active",
            chip_balance=league.starting_chip_balance,
        )

        db.add(owner_membership)

        await db.commit()
        await db.refresh(league)

    except Exception:
        await db.rollback()
        raise

    return league

# router call to get leagues per user
@router.get("", response_model=list[LeagueResponse])
async def get_leagues(
        current_user: User = Depends(get_current_user), 
        db: AsyncSession = Depends(get_db),
    ):
    
    """Fetches all leagues from the Supabase database."""
    
    statement = (
        
        select(League)
        .join(LeagueMembership, League.id == LeagueMembership.league_id)
        .where(LeagueMembership.user_id == current_user.id)
    )
    result = await db.execute(statement)
    leagues = result.scalars().all()

    return leagues



# router to retrieve league information when user is in that league
@router.get(
    "/{league_id}",
    response_model=LeagueResponse,
    )
async def get_league(
    league_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Fetches a specific league by its ID from the Supabase database, as long as user is member in legaue"""
    
    statement = (
        select(League)
        .join(LeagueMembership, League.id == LeagueMembership.league_id)
        .where(
            League.id == league_id,
            LeagueMembership.user_id == current_user.id,
            LeagueMembership.status == "active"
        )
    )
    
    result = await db.execute(statement)
    league = result.scalar_one_or_none()
    
    # Raise a 404 error if the league is not found or the user is not a member of the league.
    if league is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League not found or user is not a member of the league.",
        )
    
    return league
