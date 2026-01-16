from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# DATABASE_URL이 없으면 SQLite 사용 (개발용)
database_url = settings.database_url or "sqlite:///./usc_class_helper.db"
if not database_url.startswith("postgresql") and not database_url.startswith("sqlite"):
    print(f"⚠️ Warning: Invalid DATABASE_URL format: {database_url[:20]}...")
    database_url = "sqlite:///./usc_class_helper.db"

engine = create_engine(database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
