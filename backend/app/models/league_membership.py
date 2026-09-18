import uuid
from datetime import datetime
from typing import TYPE_CHECKING

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
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.league import League
    from app.models.user import User


class LeagueMembership(Base):
    """Represents a user's membership in a poker league."""

    __tablename__ = "league_memberships"

    __table_args__ = (
        UniqueConstraint(
            "league_id",
            "user_id",
            name="league_memberships_league_user_unique",
        ),
        CheckConstraint(
            "chip_balance >= 0",
            name="league_memberships_chip_balance_nonnegative",
        ),
        CheckConstraint(
            "role in ('owner', 'admin', 'member')",
            name="league_memberships_role_valid",
        ),
        CheckConstraint(
            "status in ('active', 'invited', 'suspended', 'left')",
            name="league_memberships_status_valid",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    league_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leagues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="member",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="active",
    )

    chip_balance: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0",
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="league_memberships",
    )

    league: Mapped["League"] = relationship(
        back_populates="memberships",
    )