# Working with the Leagues Table from Supabase, Routing it to our FastAPI backend.
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.models.league import League
from uuid import UUID

from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file

router = APIRouter(
    prefix="/leagues",
    tags=["Leagues"]
)

@router.get("/")
async def get_leagues(db: AsyncSession = Depends(get_db)):
    """Fetches all leagues from the Supabase database."""
    result = await db.execute(select(League))
    leagues = result.scalars().all()

    return leagues

@router.get("/{league_id}")
async def get_league(
    league_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Fetches a specific league by its ID from the Supabase database."""
    result = await db.execute(
        select(League).where(League.id == league_id)
    )
    return result.scalar_one_or_none()
