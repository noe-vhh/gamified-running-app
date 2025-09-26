from datetime import datetime, timedelta
import argparse
from sqlmodel import Session, select
from backend.db import engine
from backend.models.user import User
from backend.models.challenge import Challenge
from backend.models.user_challenge import UserChallenge

DEFAULT_TIERS = ["Sprint", "Marathon", "Ultra"]
DEFAULT_CHALLENGE_CONFIG = {
    "Sprint": {"distance_target_km": 5, "duration_days": 7},
    "Marathon": {"distance_target_km": 10, "duration_days": 7},
    "Ultra": {"distance_target_km": 15, "duration_days": 7}
}
DEFAULT_STREAK_DAYS = 3  # simulate a 3-day streak


def seed_user_challenges(user_id: int, mode: str = "new"):
    """
    Seed default challenges for a user with simulated streaks.
    :param user_id: ID of the user
    :param mode: "new" = assign missing challenges, "refresh" = delete and reseed
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print(f"❌ User with ID {user_id} not found")
            return

        # --- Refresh mode: delete existing UserChallenges ---
        if mode == "refresh":
            stmt = select(UserChallenge).where(UserChallenge.user_id == user_id)
            existing_ucs = session.exec(stmt).all()
            for uc in existing_ucs:
                session.delete(uc)
            session.commit()
            print(f"♻️  Deleted {len(existing_ucs)} existing challenges for user '{user.username}'")

        # --- Create default challenges if missing ---
        existing_challenges = session.exec(select(Challenge)).all()
        if not existing_challenges:
            print("🆕 No challenges found. Creating default challenges...")
            for tier in DEFAULT_TIERS:
                config = DEFAULT_CHALLENGE_CONFIG[tier]
                start_date = datetime.utcnow()
                end_date = start_date + timedelta(days=config["duration_days"])
                challenge = Challenge(
                    name=f"{tier} Challenge",
                    tier=tier,
                    type="solo",
                    sport="running",
                    distance_target_km=config["distance_target_km"],
                    start_date=start_date,
                    end_date=end_date,
                    active=True
                )
                session.add(challenge)
            session.commit()
            existing_challenges = session.exec(select(Challenge)).all()
            print(f"✅ Created {len(existing_challenges)} default challenges")

        # --- Assign challenges to user ---
        assigned_count = 0
        for challenge in existing_challenges:
            # Skip if already assigned (unless refresh mode)
            if mode == "new":
                exists = session.exec(
                    select(UserChallenge).where(
                        UserChallenge.user_id == user_id,
                        UserChallenge.challenge_id == challenge.id
                    )
                ).first()
                if exists:
                    continue

            # Simulate multiple days of streak
            streak_start_date = datetime.utcnow() - timedelta(days=DEFAULT_STREAK_DAYS)
            uc = UserChallenge(
                user_id=user.id,
                challenge_id=challenge.id,
                distance_completed_km=0.0,
                streak=DEFAULT_STREAK_DAYS,
                xp_earned=0.0,
                completed=False,
                updated_at=streak_start_date,
                joined_at=datetime.utcnow()
            )
            session.add(uc)
            assigned_count += 1

        session.commit()
        print(f"✅ Assigned {assigned_count} challenges to user '{user.username}' (ID: {user.id}) with {DEFAULT_STREAK_DAYS}-day streaks")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed challenges for a user.")
    parser.add_argument("user_id", type=int, help="The ID of the user")
    parser.add_argument(
        "--mode",
        choices=["new", "refresh"],
        default="new",
        help="Mode: 'new' = assign missing challenges, 'refresh' = delete and reseed"
    )
    args = parser.parse_args()

    seed_user_challenges(args.user_id, mode=args.mode)