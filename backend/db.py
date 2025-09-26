from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os

# Project root
BASE_DIR = Path(__file__).resolve().parents[1]  # backend/.. = project root
DATABASE_FILE = BASE_DIR / "dev.db"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_FILE}")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session