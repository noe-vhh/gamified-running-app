from backend.db import engine
from backend.models.user import User
from sqlmodel import Session, select

with Session(engine) as session:
    users = session.exec(select(User)).all()
    for u in users:
        print(u)