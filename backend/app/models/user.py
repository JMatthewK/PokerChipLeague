import uuid
from datetime import datetime

from sqlalchemy import DateTime, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """
    Application user associated with an AWS Cognito identity.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    cognito_sub: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    email: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    display_name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    """
    League relationships that haven't been integrated yet
    
    owned_leagues: Mapped[list["League"]] = relationship(
        back_populates="owner",
    )

    league_memberships: Mapped[list["LeagueMembership"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    """