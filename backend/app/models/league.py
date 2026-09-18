from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class League(Base):
    __tablename__ = "leagues"

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
        Integer,
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
