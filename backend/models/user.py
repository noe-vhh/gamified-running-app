from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Strava athlete id (unique constraint)
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

    # tokens (MVP: stored as plain text — encrypt in production)
    access_token: Optional[str] = Field(default=None)
    refresh_token: Optional[str] = Field(default=None)
    token_expires_at: Optional[datetime] = Field(default=None, sa_column=Column("token_expires_at", DateTime))

    # gamification fields
    xp: int = Field(default=0)
    momentum: int = Field(default=0)

    badges: Optional[str] = Field(default=None)   # store JSON string for MVP
    titles: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column("updated_at", DateTime))
    last_sync_at: Optional[datetime] = Field(default_factory=datetime.utcnow)