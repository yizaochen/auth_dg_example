from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()

# check the folder containing the database file exists
if not Path(settings.DB_PATH).parent.exists():
    Path(settings.DB_PATH).parent.mkdir(parents=True)


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
