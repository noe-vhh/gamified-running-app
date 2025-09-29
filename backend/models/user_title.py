from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

if TYPE_CHECKING:
    from .user import User
    from .title import Title

class UserTitle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title_id: int = Field(foreign_key="title.id")
    earned_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("earned_at", DateTime))
    is_active: bool = Field(default=False)
    
    user: Optional["User"] = Relationship(back_populates="user_titles")
    title: Optional["Title"] = Relationship(back_populates="user_titles")
