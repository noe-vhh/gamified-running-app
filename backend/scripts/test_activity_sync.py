from sqlmodel import Session, select
from backend.db import engine
from backend.models.user import User
from backend.models.user_challenge import UserChallenge
from backend.models.challenge import Challenge
from backend.services.gamification import update_challenge_progress
from backend.services.awards import award_badges_and_titles
from datetime import datetime, timedelta
from sqlalchemy.orm import selectinload

# -------------------------
# MOCK fetch_user_activities
# -------------------------
def mock_fetch_user_activities(user, after_timestamp=None):
    """
    Return fake activities for testing badges/titles.
    Each activity has 'type', 'distance' (meters), 'start_date'.
    """
    now = datetime.utcnow()
    activities = [
        {"type": "Run", "distance": 5000, "start_date": now - timedelta(days=1)},   # 5 km
        {"type": "Run", "distance": 7000, "start_date": now - timedelta(days=2)},   # 7 km
        {"type": "Run", "distance": 12000, "start_date": now - timedelta(days=3)},  # 12 km
        {"type": "Ride", "distance": 20000, "start_date": now - timedelta(days=1)}  # ignored
    ]
    if after_timestamp:
        activities = [a for a in activities if a["start_date"].timestamp() > after_timestamp]
    return activities

# -------------------------
# TEST FUNCTION
# -------------------------
def test_activity_sync(user_id: int, user_type: str = "new"):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print("User not found")
            return

        # --- For testing: always use all mock activities ---
        activities = mock_fetch_user_activities(user, after_timestamp=None)

        # --- fetch UserChallenge with preloaded challenge relationships ---
        user_challenges = session.exec(
            select(UserChallenge)
            .where(UserChallenge.user_id == user.id)
            .options(selectinload(UserChallenge.challenge))
        ).all()

        total_xp_added = 0

        print(f"\n=== Testing as {user_type.upper()} user ===")
        print(f"Processing {len(activities)} activities for user '{user.username}'\n")

        for uc in user_challenges:
            challenge = uc.challenge
            if not challenge:
                continue

            challenge_xp = 0
            print(f"Challenge: {challenge.name} | Tier: {challenge.tier}")
            for activity in activities:
                if activity["type"] != "Run":
                    continue
                distance_km = activity["distance"] / 1000
                xp = update_challenge_progress(uc, distance_km, challenge.tier)
                challenge_xp += xp
                print(f"  Activity: {distance_km} km → XP: {xp} | Streak: {uc.streak}")

            if challenge_xp > 0:
                print(f"Total XP for this challenge: {challenge_xp} | Distance completed: {uc.distance_completed_km} km | Completed: {uc.completed}\n")

            total_xp_added += challenge_xp
            uc.updated_at = datetime.utcnow()
            session.add(uc)

        # --- update user ---
        user.xp += total_xp_added
        user.momentum += total_xp_added // 10
        user.last_sync_at = datetime.utcnow()

        # --- award badges and titles ---
        new_badges, new_titles = award_badges_and_titles(user, user_challenges)

        session.add(user)
        session.commit()

        print(f"User XP added: {total_xp_added}")
        print(f"User total XP: {user.xp}")
        print(f"User momentum: {user.momentum}")
        print(f"New badges: {new_badges}")
        print(f"New titles: {new_titles}")
        print(f"Updated last_sync_at: {user.last_sync_at}\n")

# -------------------------
# RUN TEST
# -------------------------
if __name__ == "__main__":
    test_user_id = 1  # replace with your test user ID
    test_activity_sync(test_user_id, user_type="new")
    test_activity_sync(test_user_id, user_type="existing")