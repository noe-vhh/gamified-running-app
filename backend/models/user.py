from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

if TYPE_CHECKING:
    from .user_challenge import UserChallenge
    from .user_badge import UserBadge
    from .user_title import UserTitle

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    strava_athlete_id: int = Field(sa_column=Column("strava_athlete_id", Integer, unique=True, index=True))
    username: Optional[str] = Field(default=None, sa_column=Column("username", String, index=True))
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    sex: Optional[str] = Field(default=None)
    premium: Optional[bool] = Field(default=None)
    weight: Optional[float] = Field(default=None)
    profile: Optional[str] = Field(default=None)
    profile_medium: Optional[str] = Field(default=None)
    access_token: Optional[str] = Field(default=None)
    refresh_token: Optional[str] = Field(default=None)
    token_expires_at: Optional[datetime] = Field(default=None, sa_column=Column("token_expires_at", DateTime))
    xp: int = Field(default=0)
    momentum: int = Field(default=0)
    total_distance_km: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column("updated_at", DateTime))
    last_sync_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    user_challenges: List["UserChallenge"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    user_badges: List["UserBadge"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    user_titles: List["UserTitle"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

User.update_forward_refs()