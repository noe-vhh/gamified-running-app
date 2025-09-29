from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

class UserChallenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    challenge_id: int = Field(foreign_key="challenge.id")
    distance_completed_km: float = Field(default=0)
    streak: int = Field(default=0)
    completed: bool = Field(default=False)
    xp_earned: float = Field(default=0)
    joined_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(
        back_populates="user_challenges",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    challenge: "Challenge" = Relationship(
        back_populates="user_challenges",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

UserChallenge.update_forward_refs()