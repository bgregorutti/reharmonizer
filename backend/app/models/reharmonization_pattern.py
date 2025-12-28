from sqlalchemy import Column, Integer, String, ARRAY, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ReharmonizationPattern(Base):
    """Reharmonization pattern model - stores common reharmonization patterns."""

    __tablename__ = "reharmonization_patterns"

    id = Column(Integer, primary_key=True, index=True)
    pattern_name = Column(String(100), nullable=False)
    original_progression = Column(ARRAY(String(100)), nullable=False)
    reharmonized_progression = Column(ARRAY(String(100)), nullable=False)
    genre = Column(String(50), nullable=True, index=True)
    complexity_level = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(ARRAY(String(50)), nullable=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ReharmonizationPattern {self.pattern_name}>"
