from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime
from typing import List

from ..utils.dependencies import get_current_user
from ..services.strava_service import fetch_user_activities
from ..services.gamification import update_challenge_progress
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

    Syncing rules:
    - New users (no last_sync_at) → only fetch NEW activities after registration
    - Returning users → fetch activities since last sync
    """

    # Determine timestamp cutoff for fetching activities
    after_timestamp = int(current_user.last_sync_at.timestamp()) if current_user.last_sync_at else int(current_user.created_at.timestamp())

    # Fetch Strava activities
    activities = fetch_user_activities(current_user, after_timestamp=after_timestamp)

    total_xp_added = 0
    updated_challenges = []

    # Get all challenges the user is currently participating in
    user_challenges: List[UserChallenge] = session.exec(
        select(UserChallenge).where(UserChallenge.user_id == current_user.id)
    ).all()

    for uc in user_challenges:
        challenge = session.get(Challenge, uc.challenge_id)
        if not challenge:
            continue

        challenge_xp = 0

        for activity in activities:
            # Only running activities count
            if activity.get("type") != "Run":
                continue

            distance_km = activity.get("distance", 0) / 1000  # meters → km
            xp = update_challenge_progress(uc, distance_km, challenge.tier)
            challenge_xp += xp

        # Mark challenge as completed if target distance reached
        if uc.distance_completed_km >= challenge.distance_target_km:
            uc.completed = True

        if challenge_xp > 0:
            updated_challenges.append({
                "user_challenge_id": uc.id,
                "distance_completed_km": uc.distance_completed_km,
                "xp_earned": uc.xp_earned,
                "completed": uc.completed,
                "streak": uc.streak
            })

        # Always update challenge timestamp
        uc.updated_at = datetime.utcnow()
        session.add(uc)

        total_xp_added += challenge_xp

    # Update user stats
    current_user.xp += total_xp_added
    current_user.momentum += total_xp_added // 10  # Example: 10% of XP as momentum
    current_user.last_sync_at = datetime.utcnow()

    # Award achievements
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