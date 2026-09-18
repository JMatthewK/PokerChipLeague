from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User  
    from app.models.league_membership import LeagueMembership  

class League(Base):
    __tablename__ = "leagues"
    
    __table_args__ = (
        CheckConstraint(
            "starting_chip_balance >= 0",
            name="leagues_starting_chip_balance_nonnegative",
        ),
        CheckConstraint(
            "status in ('active', 'archived')",
            name="leagues_status_valid",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    status: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    owner_user_id: Mapped[UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    starting_chip_balance: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    archived_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    owner: Mapped["User"] = relationship(
        back_populates="owned_leagues",
    )

    memberships: Mapped[list["LeagueMembership"]] = relationship(
        back_populates="league",
        cascade="all, delete-orphan",
    )
