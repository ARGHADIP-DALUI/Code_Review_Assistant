from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.code_review import Base

DATABASE_URL = "sqlite:///./app/code_reviews.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create DB tables
def init_db():
    Base.metadata.create_all(bind=engine)
