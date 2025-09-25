from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime

from ..routes.users import get_current_user
from ..services.strava_service import fetch_user_activities
from ..services.gamification import update_challenge_progress
from ..db import get_session
from ..models.user_challenge import UserChallenge
from ..models.challenge import Challenge
from ..models.user import User

router = APIRouter()

@router.post("/sync")
def sync_activities(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Determine timestamp to fetch activities
    after_timestamp = int(current_user.last_sync_at.timestamp()) if current_user.last_sync_at else int(datetime.utcnow().timestamp())

    # Fetch activities from Strava after last sync
    activities = fetch_user_activities(current_user, after_timestamp=after_timestamp)

    total_xp_added = 0
    updated_challenges = []

    for uc in session.exec(select(UserChallenge).where(UserChallenge.user_id == current_user.id)).all():
        challenge = session.get(Challenge, uc.challenge_id)
        if not challenge:
            continue

        challenge_xp = 0
        for activity in activities:
            if activity.get("type") != "Run":  # MVP only running
                continue
            distance_km = activity.get("distance", 0) / 1000  # meters to km
            xp = update_challenge_progress(uc, distance_km, challenge.tier)
            challenge_xp += xp

        if challenge_xp > 0:
            updated_challenges.append(uc.id)

        # Update UserChallenge timestamp
        uc.updated_at = datetime.utcnow()
        session.add(uc)

        # Update User XP and momentum
        total_xp_added += challenge_xp

    current_user.xp += total_xp_added
    current_user.momentum += total_xp_added // 10  # example: momentum = 10% XP
    current_user.last_sync_at = datetime.utcnow()
    session.add(current_user)
    session.commit()

    return {
        "message": "Activities synced",
        "activities_count": len(activities),
        "xp_added": total_xp_added,
        "challenges_updated": updated_challenges
    }