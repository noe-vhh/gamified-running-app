from backend.db import engine
from sqlmodel import Session, select
from backend.models import User, UserChallenge, Challenge

def list_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            print(f"User: {user.username}, XP: {user.xp}, Momentum: {user.momentum}")
            # Optionally list challenges
            for uc in getattr(user, "user_challenges", []):
                print(f"  Challenge ID: {uc.challenge_id}, Distance Completed: {uc.distance_completed_km} km")

if __name__ == "__main__":
    list_users()
