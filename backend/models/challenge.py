from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Challenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    description: Optional[str] = None
    tier: str  # Sprint, Marathon, Ultra, Trailblazer
    type: str  # Solo, Public, Club
    sport: str = "running"  # default to running for MVP
    start_date: datetime
    end_date: datetime
    distance_target_km: Optional[float] = None  # e.g., 5, 7, 10 km per day/week
    active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None