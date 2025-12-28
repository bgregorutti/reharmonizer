from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class SubstitutionRule(Base):
    """Substitution rule model - stores chord substitution rules and patterns."""

    __tablename__ = "substitution_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String(100), nullable=False)
    rule_type = Column(String(50), nullable=False, index=True)
    source_chord_pattern = Column(String(50), nullable=False)
    target_chord_pattern = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    conditions = Column(JSON, nullable=True)
    priority = Column(Integer, default=1)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<SubstitutionRule {self.rule_name}>"
