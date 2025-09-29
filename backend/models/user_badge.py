from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

if TYPE_CHECKING:
    from .user import User
    from .badge import Badge

class UserBadge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    badge_id: int = Field(foreign_key="badge.id")
    earned_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("earned_at", DateTime))
    
    user: Optional["User"] = Relationship(back_populates="user_badges")
    badge: Optional["Badge"] = Relationship(back_populates="user_badges")
