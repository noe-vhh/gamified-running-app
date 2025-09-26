from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta

from backend.db import engine
from backend.models.user import User
from backend.models.user_challenge import UserChallenge
from backend.services.gamification import update_challenge_progress
from backend.services.awards import award_badges_and_titles

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
    """
    Simulate syncing user activities for testing XP, streaks, badges, and titles.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print(f"❌ User with ID {user_id} not found")
            return

        # --- Determine if streaks should be reset ---
        reset_streak = user_type.lower() == "new"

        # --- Fetch mock activities ---
        activities = mock_fetch_user_activities(user, after_timestamp=None)
        activities.sort(key=lambda a: a["start_date"])  # process chronologically

        # --- Fetch UserChallenges with preloaded Challenge relationships ---
        user_challenges = session.exec(
            select(UserChallenge)
            .where(UserChallenge.user_id == user.id)
            .options(selectinload(UserChallenge.challenge))
        ).all()

        # Reset streaks and progress for "new" users
        if reset_streak:
            for uc in user_challenges:
                uc.streak = 0
                uc.distance_completed_km = 0
                uc.xp_earned = 0
                uc.completed = False
                uc.updated_at = None

        total_xp_added = 0
        print(f"\n=== Testing as {user_type.upper()} user ===")
        print(f"Processing {len(activities)} activities for user '{user.username}'\n")

        # --- Process each challenge ---
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
                activity_date = activity.get("start_date", datetime.utcnow())
                xp = update_challenge_progress(uc, distance_km, challenge.tier, activity_date)
                challenge_xp += xp
                print(f"  Activity: {distance_km:.1f} km → XP: {xp:.1f} | Streak: {uc.streak}")

            if challenge_xp > 0:
                print(f"Total XP for this challenge: {challenge_xp:.1f} | Distance completed: {uc.distance_completed_km:.1f} km | Completed: {uc.completed}\n")

            total_xp_added += challenge_xp
            session.add(uc)

        # --- Update user stats ---
        user.xp += total_xp_added
        user.momentum += total_xp_added // 10
        user.last_sync_at = datetime.utcnow()

        # --- Award badges and titles ---
        new_badges, new_titles = award_badges_and_titles(user, user_challenges)

        session.add(user)
        session.commit()

        # --- Summary output ---
        print(f"✅ User '{user.username}' sync complete")
        print(f"Total XP added: {total_xp_added}")
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