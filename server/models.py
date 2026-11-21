from sqlalchemy import Column, Integer, String, Text, DateTime, func
from server.database import Base


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    prompt = Column(Text, nullable=False)
    response_a = Column(Text, nullable=False)
    response_b = Column(Text, nullable=False)
    category = Column(String(255), nullable=False, index=True)
    annotator_id = Column(String(255), nullable=True, index=True)
    chosen = Column(String(50), nullable=True)  # 'A', 'B', 'tie', 'skip'
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    labeled_at = Column(DateTime(timezone=True), nullable=True)
    pair_id = Column(Integer, nullable=True, index=True)

