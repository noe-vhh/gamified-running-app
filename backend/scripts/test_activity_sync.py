from datetime import datetime, timedelta
from sqlmodel import Session, select
from backend.db import engine
from backend.models.user import User
from backend.models.challenge import Challenge
from backend.models.user_challenge import UserChallenge
from backend.services.gamification import update_challenge_progress

# -------------------------
# MOCK fetch_user_activities
# -------------------------
def mock_fetch_user_activities(user, after_timestamp=None):
    """
    Return fake activities for testing.
    Each activity has 'type' and 'distance' (meters)
    """
    now = datetime.utcnow()
    activities = [
        {"type": "Run", "distance": 5000, "start_date": now - timedelta(days=1)},  # 5 km
        {"type": "Run", "distance": 7000, "start_date": now - timedelta(days=2)},  # 7 km
        {"type": "Ride", "distance": 20000, "start_date": now - timedelta(days=1)}  # ignored
    ]
    if after_timestamp:
        activities = [a for a in activities if a["start_date"].timestamp() > after_timestamp]
    return activities

# -------------------------
# TEST SYNC FUNCTION
# -------------------------
def test_activity_sync(user_id: int, scenario: str = "new"):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print("User not found")
            return

        # Simulate new vs existing user
        if scenario == "new":
            # New user: set last_sync_at to 2.5 days ago to include recent mock activities
            user.last_sync_at = datetime.utcnow() - timedelta(days=2, hours=12)
        elif scenario == "existing":
            # Existing user: last sync 3 days ago
            user.last_sync_at = datetime.utcnow() - timedelta(days=3)

        session.add(user)
        session.commit()

        after_timestamp = user.last_sync_at.timestamp() if user.last_sync_at else None
        activities = mock_fetch_user_activities(user, after_timestamp)

        if not activities:
            print(f"No activities to process for user '{user.username}' ({scenario})")
            return

        total_xp_added = 0
        print(f"\nProcessing {len(activities)} activities for user '{user.username}' ({scenario} user)")

        for uc in session.exec(select(UserChallenge).where(UserChallenge.user_id == user.id)).all():
            challenge = session.get(Challenge, uc.challenge_id)
            if not challenge:
                continue
            print(f"\nChallenge: {challenge.name} | Tier: {challenge.tier}")
            challenge_xp = 0
            for activity in activities:
                if activity["type"] != "Run":
                    continue
                distance_km = activity["distance"] / 1000
                xp = update_challenge_progress(uc, distance_km, challenge.tier)
                challenge_xp += xp
                print(f"  Activity: {distance_km} km → XP: {xp:.1f} | Streak: {uc.streak}")
            total_xp_added += challenge_xp
            print(f"Total XP for this challenge: {challenge_xp:.1f} | Distance completed: {uc.distance_completed_km:.1f} km | Completed: {uc.completed}")

            uc.updated_at = datetime.utcnow()
            session.add(uc)

        # Update user XP, momentum, last_sync_at
        user.xp += total_xp_added
        user.momentum += total_xp_added // 10
        user.last_sync_at = datetime.utcnow()
        session.add(user)
        session.commit()

        print(f"\nUser XP added: {total_xp_added:.1f}")
        print(f"User total XP: {user.xp}")
        print(f"User momentum: {user.momentum}")
        print(f"Updated last_sync_at: {user.last_sync_at}")

# -------------------------
# RUN TEST
# -------------------------
if __name__ == "__main__":
    test_user_id = 1  # replace with your test user ID
    print("=== Testing as NEW user ===")
    test_activity_sync(test_user_id, scenario="new")

    print("\n=== Testing as EXISTING user ===")
    test_activity_sync(test_user_id, scenario="existing")