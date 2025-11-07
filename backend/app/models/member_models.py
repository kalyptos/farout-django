from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from ..db import Base


class Member(Base):
    """Member model for organization members (stored in farout database)"""
    __tablename__ = "members"
    __table_args__ = {'schema': 'public'}  # farout database
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    discord_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rank: Mapped[str] = mapped_column(String(50), default='member', nullable=False, index=True)
    missions_completed: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    trainings_completed: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        Index('idx_members_discord_id', 'discord_id'),
        Index('idx_members_rank', 'rank'),
        {'schema': 'public'}
    )
