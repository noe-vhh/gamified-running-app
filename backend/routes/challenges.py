from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from ..db import get_session
from ..models.challenge import Challenge
from ..models.user_challenge import UserChallenge
from ..models.user import User
from ..routes.users import get_current_user

router = APIRouter()

# List challenges (filter optional)
@router.get("/", response_model=List[Challenge])
def list_challenges(tier: str = None, type: str = None, sport: str = None, session: Session = Depends(get_session)):
    query = select(Challenge).where(Challenge.active == True)
    if tier:
        query = query.where(Challenge.tier == tier)
    if type:
        query = query.where(Challenge.type == type)
    if sport:
        query = query.where(Challenge.sport == sport)
    return session.exec(query).all()

# Join challenge
@router.post("/{challenge_id}/join")
def join_challenge(challenge_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # check challenge exists
    challenge = session.get(Challenge, challenge_id)
    if not challenge or not challenge.active:
        raise HTTPException(status_code=404, detail="Challenge not found or inactive")

    # check if already joined
    existing = session.exec(select(UserChallenge).where(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == challenge_id
    )).first()

    if existing:
        return {"message": "Already joined", "user_challenge_id": existing.id}

    user_challenge = UserChallenge(
        user_id=current_user.id,
        challenge_id=challenge_id
    )
    session.add(user_challenge)
    session.commit()
    session.refresh(user_challenge)
    return {"message": "Challenge joined", "user_challenge_id": user_challenge.id}

# List user's joined challenges
@router.get("/my", response_model=List[UserChallenge])
def my_challenges(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(UserChallenge).where(UserChallenge.user_id == current_user.id)).all()