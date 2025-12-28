from sqlalchemy import Column, Integer, String, ARRAY, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ChordExtension(Base):
    """Chord extension model - stores possible extensions for chord qualities."""

    __tablename__ = "chord_extensions"

    id = Column(Integer, primary_key=True, index=True)
    base_quality = Column(String(20), nullable=False)
    extension_name = Column(String(50), nullable=False)
    intervals = Column(ARRAY(Integer), nullable=False)
    symbol_suffix = Column(String(20), nullable=False)
    common_usage = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ChordExtension {self.base_quality} + {self.extension_name}>"
