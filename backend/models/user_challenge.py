from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserChallenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    challenge_id: int = Field(foreign_key="challenge.id")
    
    # progress fields
    distance_completed_km: float = 0.0
    xp_earned: int = 0
    streak: int = 0  # consecutive days
    completed: bool = False

    joined_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None