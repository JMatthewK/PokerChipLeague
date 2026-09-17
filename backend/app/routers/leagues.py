# Working with the Leagues Table from Supabase, Routing it to our FastAPI backend.
from fastapi import APIRouter, Request
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file

router = APIRouter(
    prefix="/leagues",
    tags=["Leagues"]
)

@router.get("/")
async def get_leagues():
    """Fetches all leagues from the Supabase database."""
    pass