from datetime import datetime, timedelta
from sqlmodel import Session, select
from backend.db import engine
from backend.models.user import User
from backend.models.challenge import Challenge
from backend.models.user_challenge import UserChallenge

def seed_user_challenges(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print("User not found")
            return

        # Create some challenges if they don't exist
        existing_challenges = session.exec(select(Challenge)).all()
        if not existing_challenges:
            tiers = ["Sprint", "Marathon", "Ultra"]
            for tier in tiers:
                start_date = datetime.utcnow()
                end_date = start_date + timedelta(days=7)  # default 1-week challenge
                challenge = Challenge(
                    name=f"{tier} Challenge",
                    tier=tier,
                    type="solo",  
                    sport="running",
                    distance_target_km=5 if tier=="Sprint" else 10 if tier=="Marathon" else 15,
                    start_date=start_date,
                    end_date=end_date,
                    created_at=start_date,
                    active=True
                )
                session.add(challenge)
            session.commit()

            existing_challenges = session.exec(select(Challenge)).all()

        # Assign challenges to user
        for challenge in existing_challenges:
            uc = UserChallenge(
                user_id=user.id,
                challenge_id=challenge.id,
                distance_completed_km=0.0,
                streak=0,
                xp_earned=0.0,
                completed=False,
                updated_at=datetime.utcnow()
            )
            session.add(uc)
        session.commit()
        print(f"Seeded {len(existing_challenges)} challenges for user '{user.username}'")

if __name__ == "__main__":
    test_user_id = 1  # replace with your user ID
    seed_user_challenges(test_user_id)