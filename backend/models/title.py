from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
import enum

if TYPE_CHECKING:
    from .user_title import UserTitle

class TitleRarity(str, enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class Title(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(sa_column=Column(Text))
    requirements: str = Field(sa_column=Column(Text))
    rarity: TitleRarity = Field(sa_column=Column(Enum(TitleRarity)))
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column("updated_at", DateTime))

    user_titles: List["UserTitle"] = Relationship(back_populates="title")
