from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from tabulate import tabulate  # pip install tabulate

from backend.db import engine
from backend.models.user import User
from backend.models.user_challenge import UserChallenge
from backend.services.gamification import update_challenge_progress
from backend.services.awards import award_badges_and_titles
from backend.services.strava_service import fetch_user_activities

# -------------------------
# MOCK fetch_user_activities
# -------------------------
def mock_fetch_user_activities(user, after_timestamp=None):
    now = datetime.utcnow()
    activities = [
        {"type": "Run", "distance": 5000, "start_date": now - timedelta(days=1)},
        {"type": "Run", "distance": 7000, "start_date": now - timedelta(days=2)},
        {"type": "Run", "distance": 12000, "start_date": now - timedelta(days=3)},
        {"type": "Ride", "distance": 20000, "start_date": now - timedelta(days=1)}
    ]
    if after_timestamp is not None and after_timestamp > 0:
        activities = [a for a in activities if a["start_date"].timestamp() > after_timestamp]
    return activities

# -------------------------
# TEST FUNCTION
# -------------------------
def test_activity_sync(user_id: int, use_mock: bool = True, user_type: str = "new"):
    """
    Simulate syncing user activities for testing XP, streaks, badges, and titles.
    Displays a table summary per challenge.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print(f"❌ User with ID {user_id} not found")
            return

        reset_streak = user_type.lower() == "new"
        after_timestamp = int(user.last_sync_at.timestamp()) if user.last_sync_at else int(user.created_at.timestamp())

        # New users always fetch all activities
        if reset_streak:
            activities = mock_fetch_user_activities(user, after_timestamp=None) if use_mock else fetch_user_activities(user)
        else:
            activities = mock_fetch_user_activities(user, after_timestamp) if use_mock else fetch_user_activities(user, after_timestamp)

        activities.sort(key=lambda a: a["start_date"])

        user_challenges = session.exec(
            select(UserChallenge)
            .where(UserChallenge.user_id == user.id)
            .options(selectinload(UserChallenge.challenge))
        ).all()

        if reset_streak:
            for uc in user_challenges:
                uc.streak = 0
                uc.distance_completed_km = 0
                uc.xp_earned = 0
                uc.completed = False
                uc.updated_at = datetime.utcnow()

        total_xp_added = 0
        table_rows = []

        for uc in user_challenges:
            challenge = uc.challenge
            if not challenge:
                continue

            challenge_xp = 0

            for activity in activities:
                if activity["type"] != "Run":
                    continue
                distance_km = activity["distance"] / 1000
                activity_date = activity.get("start_date", datetime.utcnow())
                xp = update_challenge_progress(uc, distance_km, challenge.tier, activity_date)
                challenge_xp += xp

            total_xp_added += challenge_xp
            session.add(uc)

            table_rows.append([
                challenge.name,
                f"{challenge.tier}",
                f"{uc.distance_completed_km:.1f} km",  # actual progress in DB
                f"{challenge_xp:.1f}",
                uc.streak,
                "✅" if uc.completed else "❌"
            ])

        user.xp += total_xp_added
        user.momentum += total_xp_added // 10
        user.last_sync_at = datetime.utcnow()

        new_badges, new_titles = award_badges_and_titles(user, user_challenges)
        session.add(user)
        session.commit()

        # --- Console summary ---
        print(f"\n=== User '{user.username}' Sync Summary ({user_type.upper()} user) ===")
        print(f"Total activities processed: {len(activities)}")
        print(f"Total XP added: {total_xp_added}")
        print(f"User total XP: {user.xp}")
        print(f"User momentum: {user.momentum}")
        print(f"New badges: {new_badges}")
        print(f"New titles: {new_titles}")
        print(f"Last sync at: {user.last_sync_at}\n")

        print(tabulate(
            table_rows,
            headers=["Challenge", "Tier", "Distance Completed", "XP Earned", "Streak", "Completed"],
            tablefmt="fancy_grid"
        ))
        print("\n")

# -------------------------
# RUN TEST
# -------------------------
if __name__ == "__main__":
    test_user_id = 1  # replace with your test user ID
    test_activity_sync(test_user_id, use_mock=True, user_type="new")
    test_activity_sync(test_user_id, use_mock=True, user_type="existing")