from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime
from typing import List

from ..utils.dependencies import get_current_user
from ..services.strava_service import fetch_user_activities
from ..services.progress import update_challenge_progress
from ..services.awards import award_badges_and_titles
from ..db import get_session
from ..models.user_challenge import UserChallenge
from ..models.challenge import Challenge
from ..models.user import User

router = APIRouter()

@router.post("/sync")
def sync_activities(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Sync user activities from Strava and update:
    - Challenge progress
    - User XP and momentum
    - Badges and titles
    """
    # Determine timestamp cutoff for fetching activities
    after_timestamp = int(current_user.last_sync_at.timestamp()) if current_user.last_sync_at else int(current_user.created_at.timestamp())

    # Fetch Strava activities (auto refresh token inside)
    activities = fetch_user_activities(current_user, after_timestamp=after_timestamp)

    total_xp_added = 0
    updated_challenges = []

    # Fetch all UserChallenge records for the user
    user_challenges: List[UserChallenge] = session.exec(
        select(UserChallenge).where(UserChallenge.user_id == current_user.id)
    ).all()

    for uc in user_challenges:
        challenge = session.get(Challenge, uc.challenge_id)
        if not challenge:
            continue

        challenge_xp = 0
        for activity in activities:
            if activity.get("type") != "Run":
                continue

            distance_km = activity.get("distance", 0) / 1000  # meters → km
            activity_date = activity.get("start_date", datetime.utcnow())

            xp = update_challenge_progress(uc, distance_km, challenge.tier, activity_date)
            challenge_xp += xp

        if challenge_xp > 0:
            updated_challenges.append({
                "user_challenge_id": uc.id,
                "distance_completed_km": uc.distance_completed_km,
                "xp_earned": uc.xp_earned,
                "completed": uc.completed,
                "streak": uc.streak
            })

        session.add(uc)
        total_xp_added += challenge_xp

    # Update user stats
    current_user.xp += total_xp_added
    current_user.momentum += total_xp_added // 10
    current_user.last_sync_at = datetime.utcnow()

    # Award badges & titles
    new_badges, new_titles = award_badges_and_titles(current_user, user_challenges)

    session.add(current_user)
    session.commit()

    return {
        "message": "Activities synced successfully",
        "activities_count": len(activities),
        "xp_added": total_xp_added,
        "challenges_updated": updated_challenges,
        "new_badges": new_badges,
        "new_titles": new_titles
    }