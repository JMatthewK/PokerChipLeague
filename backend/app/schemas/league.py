from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LeagueCreate(BaseModel):
    """Request body for creating a league."""

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    starting_chip_balance: int = Field(
        default=1000,
        ge=0,
    )


class LeagueResponse(BaseModel):
    """League information returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    status: str
    owner_user_id: UUID
    starting_chip_balance: int
    created_at: datetime
    updated_at: datetime