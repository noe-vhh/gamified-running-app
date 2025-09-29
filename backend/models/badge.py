from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
import enum

if TYPE_CHECKING:
    from .user_badge import UserBadge

class BadgeCategory(str, enum.Enum):
    DISTANCE = "distance"
    STREAK = "streak"
    CHALLENGE = "challenge"
    SOCIAL = "social"
    SPECIAL = "special"

class Badge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(sa_column=Column(Text))
    category: BadgeCategory = Field(sa_column=Column(Enum(BadgeCategory)))
    requirements: str = Field(sa_column=Column(Text))
    icon_url: Optional[str] = Field(default=None)
    rarity: str = Field(default="common")  # common, uncommon, rare, epic, legendary
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column("updated_at", DateTime))

    user_badges: List["UserBadge"] = Relationship(back_populates="badge")
