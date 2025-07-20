from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(30), default="python")
    suggestions = Column(Text)
    warnings = Column(Text)
    optimizations = Column(Text)
    score = Column(Integer)
    remark = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
