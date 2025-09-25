from sqlmodel import Session, select
from backend.db import engine
from backend.models.user import User
from backend.models.user_challenge import UserChallenge
from backend.models.challenge import Challenge

def list_user_challenges(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print("User not found")
            return

        ucs = session.exec(select(UserChallenge).where(UserChallenge.user_id == user_id)).all()
        if not ucs:
            print(f"No challenges found for user {user.username}")
            return

        for uc in ucs:
            challenge = session.get(Challenge, uc.challenge_id)
            print(f"UserChallenge ID: {uc.id}")
            print(f"  Challenge: {challenge.name if challenge else 'None'}")
            print(f"  Tier: {challenge.tier if challenge else 'None'}")
            print(f"  Distance completed: {uc.distance_completed_km}")
            print(f"  Streak: {uc.streak}")
            print(f"  XP earned: {uc.xp_earned}")
            print(f"  Completed: {uc.completed}")
            print("------")

if __name__ == "__main__":
    test_user_id = 1  # replace with your user ID
    list_user_challenges(test_user_id)