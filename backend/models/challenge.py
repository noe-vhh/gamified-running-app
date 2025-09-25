from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Challenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tier: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user_challenges: List["UserChallenge"] = Relationship(
        back_populates="challenge",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

# Forward references
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user_challenge import UserChallenge

Challenge.update_forward_refs()