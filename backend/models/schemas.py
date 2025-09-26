from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .challenge import Challenge

class ChallengeRead(BaseModel):
    id: int
    name: str
    tier: str
    type: str
    sport: str
    distance_target_km: float
    start_date: datetime
    end_date: datetime
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserChallengeRead(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    distance_completed_km: float
    streak: int
    completed: bool
    xp_earned: float
    joined_at: datetime
    updated_at: datetime
    challenge: Optional[ChallengeRead]

    class Config:
        from_attributes = True