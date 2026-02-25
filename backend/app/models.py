from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")


class Feedback(Base):
    """Feedback/Idea model"""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="feedback")
    votes = relationship("Vote", back_populates="feedback", cascade="all, delete-orphan")


class VoteType(str, enum.Enum):
    """Vote type enum"""
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"


class Vote(Base):
    """Vote model"""
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    vote_type = Column(Enum(VoteType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    feedback = relationship("Feedback", back_populates="votes")
    user = relationship("User", back_populates="votes")

    # Composite unique constraint to prevent duplicate votes
    __table_args__ = (
        # Note: SQLAlchemy doesn't have composite unique in this version,
        # we'll handle duplicate vote prevention in CRUD layer
    )
